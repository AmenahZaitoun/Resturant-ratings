# add_facility.py
from app import create_app, db
from app.models.facilities import Facilities
from app.models.owner import Owner
from app.models.role import Role  # استيراد الدور

app = create_app()
app.app_context().push()

# إنشاء الأدوار (إذا لم تكن موجودة بعد)
owner_role = Role(name="owner")
admin_role = Role(name="admin")

db.session.add_all([owner_role, admin_role])
db.session.commit()

# إنشاء الملاك الجدد وربطهم مع الدور (owner_role)
owner1 = Owner(
    fname="Ali", lname="Mansour", username="alim", 
    email="ali@example.com", password="123456",
    role_id=owner_role.id
)

owner2 = Owner(
    fname="Sara", lname="Khaled", username="sarak", 
    email="sara@example.com", password="123456",
    role_id=owner_role.id
)

owner3 = Owner(
    fname="Omar", lname="Salim", username="omars", 
    email="omar@example.com", password="123456",
    role_id=owner_role.id
)

# أضف الملاك إلى قاعدة البيانات
db.session.add_all([owner1, owner2, owner3])
db.session.commit()

# إنشاء المنشآت وربطها مع الملاك
facility1 = Facilities(
    facility_name="Naranj",
    facility_type="restaurant",
    facility_category="luxury",
    rating=4.4,
    image="uploads/facilities/Naranj.avif",
    owner_id=owner1.id
)

facility2 = Facilities(
    facility_name="Karma",
    facility_type="cafe",
    facility_category="youth_friendly",
    rating=5.0,
    image="uploads/facilities/karma.jpg",
    owner_id=owner2.id
)

facility3 = Facilities(
    facility_name="Four Seasons",
    facility_type="hotel",
    facility_category="luxury",
    rating=5.0,
    image="uploads/facilities/fourseasons.avif",
    owner_id=owner3.id
)

# أضف المنشآت
db.session.add_all([facility1, facility2, facility3])
db.session.commit()

print("✅ Roles, Owners and Facilities added successfully!")
