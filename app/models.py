from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Example Model - JobTask
class JobTask(Base):
    __tablename__ = "jobtask"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    trackingId = Column(String(25), nullable=True)
    ecpid = Column(Integer, ForeignKey("ecp.id"), nullable=False)
    ecpcode = Column(String(25), nullable=True)
    orderCycleId = Column(Integer, ForeignKey("ordercycle.id"), nullable=True)
    tagsCategoryId = Column(Integer, ForeignKey("tagscategory.id"), nullable=True)
    totalOrder = Column(Integer, nullable=True)
    tagsBeta = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    categoryId = Column(Integer, ForeignKey("categories.id"), nullable=True)
    capture = Column(Text, nullable=True)
    jobStatus = Column(Integer, ForeignKey("jobstatus.id"), nullable=True)
    calljob = Column(String(10), nullable=True, comment='Y = User call , N = Default data')
    calluser = Column(Integer, ForeignKey("users.id"), nullable=True, comment='User On hand')
    comment = Column(Integer, ForeignKey("comment_type.id"), nullable=True)
    QCStatus = Column(Integer, ForeignKey("jobstatus.id"), nullable=True)
    callQC = Column(String(10), nullable=True)
    callQCuser = Column(String(100), nullable=True)
    commentQC = Column(Integer, ForeignKey("comment_type.id"), nullable=True)
    commentNote = Column(Text, nullable=True)
    ticketCode = Column(String(15), nullable=True)
    createdate = Column(DateTime, nullable=True)
    createuser = Column(String(255), nullable=True)
    updatedate = Column(DateTime, nullable=True)
    updateuser = Column(String(255), nullable=True)
    deldate = Column(DateTime, nullable=True)
    deluser = Column(String(255), nullable=True)
    updateqcdate = Column(DateTime, nullable=True)
    shipto = Column(String(255), nullable=True)
    callJabdate = Column(DateTime, nullable=True)

    # Relationships
    ecp = relationship("Ecp", back_populates="jobtasks")
    categories = relationship("Categories", back_populates="jobtasks")
    job_status = relationship("JobStatus", back_populates="jobtasks", foreign_keys=[jobStatus])
    qc_status = relationship("JobStatus", back_populates="qc_jobtasks", foreign_keys=[QCStatus])
    order_cycle = relationship("OrderCycle", back_populates="jobtasks")
    tags_beta = relationship("TagsBeta", back_populates="jobtask")
    tags_job = relationship("TagsJob", back_populates="jobtask")
    comment_type_comment = relationship("CommentType", 
                                      foreign_keys=[comment],
                                      backref="jobtasks_comment")
    comment_type_qc = relationship("CommentType", 
                                 foreign_keys=[commentQC],
                                 backref="jobtasks_qc")

# Example Model - Ecp
class Ecp(Base):
    __tablename__ = "ecp"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_cd = Column(String(100), nullable=True)
    customer_name = Column(String(255), nullable=True)
    payment_term_cd = Column(String(255), nullable=True, comment='1 CREDIT\n2 COD')
    customer_alert_1 = Column(String(255), nullable=True)
    customer_alert_2 = Column(String(255), nullable=True)
    customer_alert_3 = Column(String(255), nullable=True)
    promo_code = Column(String(255), nullable=True)
    bu = Column(String(100), nullable=True)
    promo_type = Column(String(255), nullable=True)
    promo_name = Column(String(255), nullable=True)
    promo_start_date = Column(DateTime, nullable=True)
    promo_end_date = Column(DateTime, nullable=True)
    promo_details = Column(String(255), nullable=True)
    customer_type = Column(String(255), nullable=True, comment='1 standard\n2 VIP')
    region = Column(String(255), nullable=True)
    routecode = Column(String(255), nullable=True)
    routename = Column(String(255), nullable=True)
    show_price = Column(String(10), nullable=True)
    leave_bill = Column(String(10), nullable=True)
    store_comment = Column(String(255), nullable=True)
    logis_remark = Column(String(255), nullable=True)
    logis_cycle = Column(Integer, nullable=True, comment='รอบจัดส่ง')
    morning_only = Column(String(10), nullable=False, comment='yes or no')
    evening_only = Column(String(10), nullable=False, comment='yes or no')
    working_day_only = Column(String(10), nullable=False, comment='yes or no')
    logis_note = Column(String(255), nullable=True)
    logis_note2 = Column(String(255), nullable=True)
    logis_delivery = Column(String(255), nullable=True)
    logis_comment = Column(String(255), nullable=True)
    c_customer_parent_group = Column(String(255), nullable=True)
    c_experts = Column(String(255), nullable=True)
    c_partner = Column(String(255), nullable=True)
    nikon_lenswear_partner = Column(String(255), nullable=True)
    upgrade_coating = Column(String(10), nullable=True)
    upgrade_azio = Column(String(10), nullable=True)
    upgrade_f360 = Column(String(100), nullable=True)
    
    
    # Relationships
    jobtasks = relationship("JobTask", back_populates="ecp")

# Example Model - TagsBeta (Linking table for JobTask and Tags)
class TagsBeta(Base):
    __tablename__ = "tagsbeta"
    
    jobid = Column(Integer, ForeignKey("jobtask.id"), primary_key=True)
    tagsid = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    # Relationships
    jobtask = relationship("JobTask", back_populates="tags_beta")
    tag = relationship("Tags", back_populates="tags_beta")

# Example Model - TagsJob (Another linking table for JobTask and Tags)
class TagsJob(Base):
    __tablename__ = "tagsjob"
    
    jobid = Column(Integer, ForeignKey("jobtask.id"), primary_key=True)
    tagsid = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    # Relationships
    jobtask = relationship("JobTask", back_populates="tags_job")
    tag = relationship("Tags", back_populates="tags_job")

# Example Model - Tags
class Tags(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String)
    text_color = Column(String)
    background_color = Column(String)

    # Relationships
    tags_beta = relationship("TagsBeta", back_populates="tag")
    tags_job = relationship("TagsJob", back_populates="tag")

# Example Model - Categories
class Categories(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    categoriesName = Column(String)

    # Relationships
    jobtasks = relationship("JobTask", back_populates="categories")

# Example Model - JobStatus
class JobStatus(Base):
    __tablename__ = "jobstatus"
    
    id = Column(Integer, primary_key=True, index=True)
    statusname = Column(String, nullable=False)

    # Relationships
    jobtasks = relationship("JobTask", back_populates="job_status", foreign_keys="[JobTask.jobStatus]")
    qc_jobtasks = relationship("JobTask", back_populates="qc_status", foreign_keys="[JobTask.QCStatus]")

# Example Model - OrderCycle
class OrderCycle(Base):
    __tablename__ = "ordercycle"
    
    id = Column(Integer, primary_key=True, index=True)
    cyclename = Column(String)

    # Relationships
    jobtasks = relationship("JobTask", back_populates="order_cycle")

class CommentType(Base):
    __tablename__ = "comment_type"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    commentName = Column(String(100), nullable=True)
    commentType = Column(String(100), nullable=True)
    commentStatus = Column(Integer, nullable=True)
    createuser = Column(String(100), nullable=True)
    createdate = Column(DateTime, nullable=True)
    updateUser = Column(String(100), nullable=True)
    updatedate = Column(DateTime, nullable=True)
    delUser = Column(String(100), nullable=True)
    deldate = Column(DateTime, nullable=True)

    # Relationships
    support_jobs = relationship("SupportJob", back_populates="comment_type")
    contact_types = relationship("ContactType", back_populates="comment_type")
    action_types = relationship("ActionType", back_populates="comment_type")

class SupportJob(Base):
    __tablename__ = "supportjob"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transactionCode = Column(String(10), nullable=True)
    ticketcode = Column(String(100), nullable=True)
    trackingNo = Column(String(255), nullable=True)
    ref_tracking = Column(String(255), nullable=True)
    contactType = Column(Integer, ForeignKey("contacttype.id"), nullable=True)
    contactName = Column(String(100), nullable=True)
    actionType = Column(Integer, ForeignKey("actiontype.id"), nullable=True)
    comment = Column(Integer, ForeignKey("comment_type.id"), nullable=True)
    createUser = Column(String(100), nullable=True)
    createDate = Column(DateTime, nullable=True)
    updateUser = Column(String(100), nullable=True)
    updateDate = Column(DateTime, nullable=True)
    deleteUser = Column(String(100), nullable=True)
    deleteDate = Column(DateTime, nullable=True)
    rejectUser = Column(String(100), nullable=True)
    rejectDate = Column(DateTime, nullable=True)
    rejectRemark = Column(String(100), nullable=True)
    status = Column(Integer, nullable=True, comment='1 = Follow\n2 = Close')

    # Relationships
    action_type = relationship("ActionType", back_populates="support_jobs")
    contact_type = relationship("ContactType", back_populates="support_jobs")
    comment_type = relationship("CommentType", back_populates="support_jobs")

class ContactType(Base):
    __tablename__ = "contacttype"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contactName = Column(String(100), nullable=True)
    commentType = Column(Integer, ForeignKey("comment_type.id"), nullable=True, comment='Table : comment_type')
    status = Column(Integer, nullable=True, comment='1: active ,  2: inactive')
    createUser = Column(String(100), nullable=True)
    createDate = Column(DateTime, nullable=True)
    updateUser = Column(String(100), nullable=True)
    updateDate = Column(DateTime, nullable=True)
    deleteUser = Column(String(100), nullable=True)
    deleteDate = Column(DateTime, nullable=True)

    # Relationships
    support_jobs = relationship("SupportJob", back_populates="contact_type")
    comment_type = relationship("CommentType", back_populates="contact_types")

class ActionType(Base):
    __tablename__ = "actiontype"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    actionName = Column(String(100), nullable=True)
    commentType = Column(Integer, ForeignKey("comment_type.id"), nullable=True)
    status = Column(Integer, nullable=True, comment='1: active, 2: inactive')
    completeFlag = Column(Integer, nullable=True, comment='1: Not Close\n2: Close Jobs')
    createUser = Column(String(100), nullable=True)
    createDate = Column(DateTime, nullable=True)
    updateUser = Column(String(100), nullable=True)
    updateDate = Column(DateTime, nullable=True)
    deleteUser = Column(String(100), nullable=True)
    deleteDate = Column(DateTime, nullable=True)

    # Relationships
    support_jobs = relationship("SupportJob", back_populates="action_type")
    comment_type = relationship("CommentType", back_populates="action_types")

# New Model - Users
class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(100), nullable=False)
    user_password = Column(String(200), nullable=False)
    user_created_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_img = Column(String(255), nullable=True)
    user_role = Column(String(100), nullable=True)
    user_branch = Column(String(10), nullable=True)
    user_position = Column(String(100), nullable=True)
    compcode = Column(String(10), nullable=True)
    mobile = Column(String(15), nullable=True)
    user_status = Column(String(20), nullable=True)
    prekey = Column(String(20), nullable=True)
    line_auth = Column(String(255), nullable=True)

    # Relationships
    # jobtasks = relationship("JobTask", back_populates="users")

