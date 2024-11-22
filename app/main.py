from sqlalchemy import func, case, select, text, or_
from sqlalchemy.orm import aliased, Session
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from app.models import  JobTask, Ecp, TagsBeta, TagsJob, Categories, JobStatus, OrderCycle, Tags, CommentType, SupportJob, Users  # import your models
# from models import JobTask, Ecp, TagsBeta, TagsJob, Categories, JobStatus, OrderCycle, Tags, CommentType, SupportJob, Users  # import your models
from typing import List  # เพิ่มการนำเข้า List
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from io import BytesIO  # เพิ่มบรรทัดนี้

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
from dotenv import load_dotenv
from app.database import SQLALCHEMY_DATABASE_URL, get_db
from fastapi.middleware.cors import CORSMiddleware
import time  # เพิ่มบรรทัดนี้
from random import randint  # เพิ่มบรรทัดนี้

# Pydantic model for JobTask response
class JobTaskResponse(BaseModel):
    id: int
    ecpcode: str
    customer_name: str
    trackingId: Optional[str]
    categoryId: Optional[int]
    tagsBeta: Optional[str]
    tagsJob: Optional[str] 
    categoriesName: Optional[str]
    createdate: str
    statusname: Optional[str]
    morning_only: Optional[bool]
    evening_only: Optional[bool]
    working_day_only: Optional[bool]
    customer_type: Optional[str]
    calljob: Optional[bool]
    capture: Optional[bool]
    jobStatus: Optional[int]
    qcstatus: Optional[bool]
    createuser: Optional[str]
    cyclename: Optional[str]
    ocid: Optional[int]
    shipto: Optional[str]
    totalOrder: Optional[int]
    ticketCode: Optional[str]

    class Config:
        # orm_mode = True
        from_attributes = True

# Pydantic model for JobTask
class JobTaskBase(BaseModel):
    ecpcode: Optional[str]
    categoriesid: Optional[int]
    id: int
    ecpid: int
    trackingId: str
    createdate: datetime
    calljob: Optional[bool]
    capture: Optional[bool]
    jobStatus: Optional[int]
    qcstatus: Optional[bool]
    createuser: Optional[str]
    orderCycleId: Optional[int]
    shipto: Optional[str]
    totalOrder: Optional[int]

    class Config:
        # orm_mode = True
        from_attributes = True

# Pydantic model for Ecp
class EcpBase(BaseModel):
    id: int
    customer_cd: Optional[str]
    customer_name: Optional[str]
    payment_term_cd: Optional[str]
    customer_alert_1: Optional[str]
    customer_alert_2: Optional[str]
    customer_alert_3: Optional[str]
    promo_code: Optional[str]
    bu: Optional[str]
    promo_type: Optional[str]
    promo_name: Optional[str]
    promo_start_date: Optional[datetime]
    promo_end_date: Optional[datetime]
    promo_details: Optional[str]
    customer_type: Optional[str]
    region: Optional[str]
    routecode: Optional[str]
    routename: Optional[str]
    show_price: Optional[str]
    leave_bill: Optional[str]
    store_comment: Optional[str]
    logis_remark: Optional[str]
    logis_cycle: Optional[int]
    morning_only: Optional[str]
    evening_only: Optional[str]
    working_day_only: Optional[str]
    logis_note: Optional[str]
    logis_note2: Optional[str]
    logis_delivery: Optional[str]
    logis_comment: Optional[str]
    c_customer_parent_group: Optional[str]
    c_experts: Optional[str]
    c_partner: Optional[str]
    nikon_lenswear_partner: Optional[str]
    upgrade_coating: Optional[str]
    upgrade_azio: Optional[str]
    upgrade_f360: Optional[str]
    

    class Config:
        # orm_mode = True
        from_attributes = True

# Pydantic model for CommentType
class CommentTypeBase(BaseModel):
    id: int
    commentName: Optional[str]
    commentType: Optional[str]
    commentStatus: Optional[int]
    createuser: Optional[str]
    createdate: Optional[datetime]
    updateUser: Optional[str]
    updatedate: Optional[datetime]
    delUser: Optional[str]
    deldate: Optional[datetime]

    class Config:
        # orm_mode = True
        from_attributes = True

# Pydantic model for SupportJob
class SupportJobBase(BaseModel):
    id: int
    transactionCode: Optional[str]
    ticketcode: Optional[str]
    trackingNo: Optional[str]
    ref_tracking: Optional[str]
    contactType: Optional[int]
    contactName: Optional[str]
    actionType: Optional[int]
    comment: Optional[int]
    createUser: Optional[str]
    createDate: Optional[datetime]
    updateUser: Optional[str]
    updateDate: Optional[datetime]
    deleteUser: Optional[str]
    deleteDate: Optional[datetime]
    rejectUser: Optional[str]
    rejectDate: Optional[datetime]
    rejectRemark: Optional[str]
    status: Optional[int]

    class Config:
        # orm_mode = True
        from_attributes = True

# Pydantic model for Users
class UsersBase(BaseModel):
    id: int
    user_name: Optional[str]
    user_email: Optional[str]
    user_password: Optional[str]
    user_created_at: Optional[datetime]
    user_img: Optional[str]
    user_role: Optional[str]
    user_branch: Optional[str]
    user_position: Optional[str]
    compcode: Optional[str]
    mobile: Optional[str]
    user_status: Optional[str]
    prekey: Optional[str]
    line_auth: Optional[str]

    class Config:
        # orm_mode = True
        from_attributes = True

load_dotenv()       
# print(os.getenv('ENV'))
# สร้าง engine และ session
DATABASE_URL = SQLALCHEMY_DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# print(DATABASE_URL)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "https://essilor.lumpsum.cloud","https://apiessilor.lumpsum.cloud","https://essilor-352c706b5445.herokuapp.com","https://essilor-352c706b5445.herokuapp.com"],  # List allowed origins
    allow_credentials=True,  # Allow cookies/auth headers
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/job-task/{sag1}")
def get_job_task(sag1: int, session: Session = Depends(get_db)):
    # สร้าง template สำหรับ tag HTML
    tag_template = "<span class='badge fs-6 mb-3' style='color: {}; background-color: {};'>{}</span>"
    
    # แก้ไขการสร้าง subquery สำหรับ tagsBeta
    tags_beta_subquery = (
        session.query(
            TagsBeta.jobid,
            func.group_concat(
                func.concat(
                    # สร้าง HTML ใน Python แทน
                    text("CONCAT('<span class=\"badge fs-6 mb-3\" style=\"color: ', tags.text_color, '; background-color: ', tags.background_color, ';\">', tags.tag_name, '</span>')")
                )
            ).label('tags')
        )
        .join(Tags, TagsBeta.tagsid == Tags.id)
        .group_by(TagsBeta.jobid)
        .subquery()
    )

    # แก้ไขการสร้าง subquery สำหรับ tagsJob 
    tags_job_subquery = (
        session.query(
            TagsJob.jobid,
            func.group_concat(
                func.concat(
                    # สร้าง HTML ใน Python แทน
                    text("CONCAT('<span class=\"badge fs-6 mb-3\" style=\"color: ', tags.text_color, '; background-color: ', tags.background_color, ';\">', tags.tag_name, '</span>')")
                )
            ).label('tags')
        )
        .join(Tags, TagsJob.tagsid == Tags.id)
        .group_by(TagsJob.jobid)
        .subquery()
    )

    # สร้าง query หลัก
    query = (
        session.query(
            JobTask.id,
            JobTask.ecpcode,
            Ecp.customer_name,
            JobTask.trackingId,
            JobTask.categoryId,
            tags_beta_subquery.c.tags.label('tagsBeta'),
            tags_job_subquery.c.tags.label('tagsJob'),
            Categories.categoriesName,
            func.date_format(JobTask.createdate, "%d/%m/%Y %H:%i").label("createdate"),
            JobStatus.statusname,
            Ecp.morning_only,
            Ecp.evening_only,
            Ecp.working_day_only,
            Ecp.customer_type,
            JobTask.calljob,
            JobTask.capture,
            JobTask.jobStatus,
            JobTask.QCStatus,  # แก้ไขจาก qcstatus เป็น QCStatus
            JobTask.createuser,
            OrderCycle.cyclename,
            JobTask.orderCycleId.label("ocid"),
            JobTask.shipto,
            JobTask.totalOrder,
        )
        .join(Ecp, JobTask.ecpid == Ecp.id)
        .outerjoin(tags_beta_subquery, JobTask.id == tags_beta_subquery.c.jobid)
        .outerjoin(tags_job_subquery, JobTask.id == tags_job_subquery.c.jobid)
        .outerjoin(Categories, JobTask.categoryId == Categories.id)
        .outerjoin(JobStatus, JobTask.jobStatus == JobStatus.id)
        .outerjoin(OrderCycle, JobTask.orderCycleId == OrderCycle.id)
    )

    # กรองข้อมูลตามพารามิเตอร์ sag1
    if sag1 == 2:
        query = query.filter(Ecp.customer_type == "VIP", JobTask.calljob.is_(None))

    # เรียงลำดับผลลัพธ์
    query = query.order_by(JobTask.createdate.asc())

    # ดึงข้อมูลและส่งกลับผลลัพธ์
    results = session.execute(query).fetchall()

    # ตรวจสอบว่ามีผลลัพธ์หรือไม่
    if results:
        columns = [col['name'] for col in query.column_descriptions]
        data = [dict(zip(columns, row)) for row in results]  # สร้างรายการข้อมูล
        json_data = {
            "recordsTotal": len(results),
            "recordsFiltered": len(results),
            "data": data
        }
        return json_data
    else:
        json_data = {
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "data": []
        }  # คืนค่ารายการว่างหากไม่มีผลลัพธ์
        return json_data

@app.get("/ecp")
async def get_ecp(
    per_page: int,
    page: int = 1,
    session: Session = Depends(get_db)
):
    try:
        # คำนวณ offset สำหรับการ pagination
        offset = (page - 1) * per_page
        
        # นับจำนวนรายการทั้งหมด
        total_count = session.query(func.count(Ecp.id)).scalar()
        
        # ดึงข้อมูลแบบ pagination และเลือกเฉพาะ columns ที่จำเป็น
        ecp_query = session.query(Ecp).order_by(Ecp.id).offset(offset).limit(per_page).all()
        
        # แปลงข้อมูลเป็น dictionary
        data = [
            {
                'id': ecp.id,
                'customer_cd': ecp.customer_cd,
                'customer_name': ecp.customer_name,
                'customer_type': ecp.customer_type,
                'payment_term_cd': ecp.payment_term_cd,
                'region': ecp.region,
                'routecode': ecp.routecode,
                'routename': ecp.routename,
                'show_price': ecp.show_price,
                'leave_bill': ecp.leave_bill,
                'store_comment': ecp.store_comment,
                'logis_remark': ecp.logis_remark,
                'logis_cycle': ecp.logis_cycle,
                'morning_only': ecp.morning_only,
                'evening_only': ecp.evening_only,
                'working_day_only': ecp.working_day_only,
                'logis_note': ecp.logis_note,
                'logis_note2': ecp.logis_note2,
                'logis_delivery': ecp.logis_delivery,
                'logis_comment': ecp.logis_comment,
                'c_customer_parent_group': ecp.c_customer_parent_group,
                'c_experts': ecp.c_experts,
                'c_partner': ecp.c_partner,
                'nikon_lenswear_partner': ecp.nikon_lenswear_partner,
                'upgrade_coating': ecp.upgrade_coating,
                'upgrade_azio': ecp.upgrade_azio,
                'upgrade_f360': ecp.upgrade_f360
            }
            for ecp in ecp_query
        ]
        
        json_data = {
            "recordsTotal": total_count,
            "recordsFiltered": total_count,
            "currentPage": page,
            "perPage": per_page,
            "data": data  # ใช้ data ที่แปลงแล้ว
        }
        return json_data
    except Exception as e:
        raise ValueError("An error occurred while fetching ECP data") from e

@app.get("/getJobtaskSupport/{sag1}/{sag2}/{sag3}/{sag4}")
async def get_jobtask_support(sag1: int, sag2: str, sag3: int, sag4: int, session: Session = Depends(get_db)):
    try:
        prefix = "TIK"

        # ปรับ query ให้เลือกเฉพาะ fields ที่จำเป็น
        code_records = (
            session.query(JobTask.id, JobTask.ticketCode, JobTask.comment)
            .filter(JobTask.ticketCode.is_(None), JobTask.comment == sag1)
            .order_by(JobTask.id.asc())
            .all()
        )
 
        if code_records:
            try:
                for record in code_records:
                    unique_number = f"{int(time.time()) % 1000000:06}{randint(100, 999)}"
                    unique_code = f"{prefix}{unique_number}"

                    # ตรวจสอบว่ามี ticketCode ซ้ำหรือไม่
                    while session.query(JobTask).filter(JobTask.ticketCode == unique_code).first():
                        unique_number = f"{int(time.time()) % 1000000:06}{randint(100, 999)}"
                        unique_code = f"{prefix}{unique_number}"

                    # อัปเดตเฉพาะ ticketCode
                    session.query(JobTask).filter(JobTask.id == record.id).update(
                        {"ticketCode": unique_code},
                        synchronize_session=False
                    )
                
                session.commit()
                # return {"status": "success", "message": "Updated successfully"}
                        # สร้าง query สำหรับดึงข้อมูล
                query = session.query(
                    JobTask.id,
                    JobTask.trackingId,
                    JobTask.ecpid,
                    JobTask.ecpcode,
                    JobTask.orderCycleId,
                    JobTask.tagsCategoryId,
                    JobTask.tagsBeta,
                    JobTask.tags,
                    JobTask.categoryId,
                    JobTask.capture,
                    JobTask.createdate,
                    JobTask.createuser,
                    JobTask.updatedate,
                    JobTask.updateuser,
                    JobTask.deldate,
                    JobTask.deluser,
                    JobTask.jobStatus,
                    JobTask.calljob,
                    JobTask.calluser,
                    JobTask.comment,
                    JobTask.QCStatus,
                    JobTask.callQC,
                    JobTask.callQCuser,
                    JobTask.commentQC,
                    JobTask.commentNote,
                    JobTask.updateqcdate,
                    Ecp.customer_cd.label('ecp_code'),
                    Ecp.customer_name,
                    CommentType.id.label('commentID'),
                    CommentType.commentName,
                    JobStatus.statusname,
                    JobTask.ticketCode,
                    func.count(SupportJob.ticketcode).label('ticketCodeCount')
                ).join(
                    Ecp, JobTask.ecpid == Ecp.id
                ).join(
                    CommentType, or_(JobTask.comment == CommentType.id, JobTask.commentQC == CommentType.id)
                ).join(
                    JobStatus, JobTask.jobStatus == JobStatus.id
                ).outerjoin(
                    SupportJob, JobTask.ticketCode == SupportJob.ticketcode
                )

                # กรองข้อมูลตามเงื่อนไข
                query = query.filter(
                    (JobTask.commentQC == sag1) if 9 <= sag1 <= 12 else (JobTask.comment == sag1),
                    func.month(JobTask.updatedate) == sag3,
                    func.year(JobTask.updatedate) == sag4,
                    (JobTask.jobStatus.notin_([11, 12]) if sag2 == 'pending' else JobTask.jobStatus.in_([11, 12]))
                )

                # จัดกลุ่มและเรียงลำดับข้อมูล
                query = query.group_by(JobTask.ticketCode).order_by(
                    func.count(SupportJob.ticketcode) >= 2, JobTask.updatedate.asc()
                )

                # ดึงข้อมูลและนับจำนวน
                result = query.all()
                count = len(result)

                # แปลงผลลัพธ์เป็น dictionary
                data = [dict(row._mapping) for row in result]
                result = {
                    "recordsTotal": count,
                    "recordsFiltered": count,
                    "data": data
                }
                return result
                
            except Exception as commit_error:
                session.rollback()
                raise HTTPException(
                    status_code=500,
                    detail=f"Error during commit: {str(commit_error)}"
                )
        
        return {"status": "success", "message": "No records to update"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )


@app.post("/import-ecp-from-excel/")
def import_ecp_from_excel(file: UploadFile = File(...), session: Session = Depends(get_db)):
    try:
        # ตรวจสอบนามสกุลไฟล์
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail="รองรับเฉพาะไฟล์ Excel (.xlsx, .xls) เท่านั้น"
            )

        # อ่านไฟล์ Excel
        file_content = file.file.read()
        df = pd.read_excel(BytesIO(file_content))
        
        # ตรวจสอบว่ามีข้อมูลในไฟล์หรือไม่
        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="ไฟล์ Excel ไม่มีข้อมูล"
            )

        # แปลงข้อมูลจาก DataFrame เป็น dict และทำความสะอาดข้อมูล
        # โดยแทนที่ค่า pd.NA ด้วย None และค่า float('nan') ด้วยสตริงว่าง
        # แปลง DataFrame เป็น list ของ dictionary โดยแต่ละ dictionary แทนแถวหนึ่งใน DataFrame
        records = df.replace({pd.NA: None, float('nan'): None}).to_dict(orient='records')
        
        success_count = 0
        error_records = []
        
        # เพิ่มข้อมูลเข้า database
        for record in records:
            try:
                # ลบ key ที่ไม่มีใน model ออก
                valid_record = {k: v for k, v in record.items() if hasattr(Ecp, k)}
                ecp = Ecp(**valid_record)
                session.add(ecp)
                success_count += 1
            except Exception as record_error:
                error_records.append({
                    "data": record,
                    "error": str(record_error)
                })
        
        session.commit()
        
        result = {
            "status": "success",
            "message": f"นำเข้าข้อมูลสำเร็จ {success_count} รายการ"
        }

        if error_records:
            result["errors"] = error_records
            result["failed_count"] = len(error_records)
            
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการนำเข้าข้อมูล: {str(e)}"
        )
    finally:
        file.file.close()


@app.get("/searchEcp")
def search_ecp(search: str, session: Session = Depends(get_db)):
    query = (
        session.query(Ecp)
        .filter(
            or_(
                Ecp.customer_name.ilike(f"%{search}%"),
                Ecp.customer_cd.ilike(f"%{search}%"),
                Ecp.c_partner.ilike(f"%{search}%"),
                Ecp.c_experts.ilike(f"%{search}%"),
                Ecp.payment_term_cd.ilike(f"%{search}%"),
                Ecp.logis_note.ilike(f"%{search}%")
            )
        )
        .all()
    )
    return {
        "recordsTotal": len(query),
        "recordsFiltered": len(query),
        "data": [ecp for ecp in query]
    }
