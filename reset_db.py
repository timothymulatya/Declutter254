from app import create_app
from extensions import db
from models import User, Category, Item, Request
from flask_bcrypt import generate_password_hash

def reset_database():
    """Reset and seed the database with MVP data"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("🗑️  Database dropped")
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Create categories
        categories = [
            Category(name="Furniture", description="Sofas, tables, beds, chairs"),
            Category(name="Kitchen", description="Pots, sufuria, utensils, plates"),
            Category(name="Electronics", description="TVs, phones, radios, laptops"),
            Category(name="Clothes", description="Children's clothes, adult clothes, shoes"),
            Category(name="Books", description="School books, novels, textbooks")
        ]
        
        db.session.add_all(categories)
        db.session.commit()
        print(f"✅ Created {len(categories)} categories")
        
        # Create users
        users = [
            User(
                phone_number="0712345678",
                password_hash=generate_password_hash("password123").decode('utf-8'),
                name="Jane Mwangi",
                location="Roysambu, near Tuskys"
            ),
            User(
                phone_number="0723456789",
                password_hash=generate_password_hash("password123").decode('utf-8'),
                name="John Otieno",
                location="Donholm, near Shell"
            ),
            User(
                phone_number="0734567890",
                password_hash=generate_password_hash("password123").decode('utf-8'),
                name="Mary Wanjiku",
                location="Lang'ata, near Oilibya"
            )
        ]
        
        db.session.add_all(users)
        db.session.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create items
        items = [
            Item(
                title="Sofa Set - 3 Seater",
                description="Brown leather sofa, still in good condition. Slightly used but very comfortable.",
                photo_url="https://via.placeholder.com/300?text=Sofa",
                condition="Good",
                pickup_location="Tuskys Roysambu",
                pickup_days="Saturdays and Sundays",
                pickup_times="10:00 - 14:00",
                special_instructions="Call when you arrive, I'll bring it outside",
                is_available=True,
                giver_id=users[0].id,
                category_id=categories[0].id
            ),
            Item(
                title="Sufuria Set - 3 pieces",
                description="Three sufuria in excellent condition. 1 large, 1 medium, 1 small.",
                photo_url="https://via.placeholder.com/300?text=Sufuria",
                condition="Like New",
                pickup_location="Shell Donholm",
                pickup_days="Weekdays after 5pm",
                pickup_times="17:00 - 19:00",
                special_instructions="I'll be at the petrol station. Look for a blue Toyota.",
                is_available=True,
                giver_id=users[1].id,
                category_id=categories[1].id
            ),
            Item(
                title="Children's Clothes Bundle",
                description="Mix of boys and girls clothes, age 3-4. About 15 pieces total.",
                photo_url="https://via.placeholder.com/300?text=Clothes",
                condition="Good",
                pickup_location="Oilibya Lang'ata",
                pickup_days="Saturday only",
                pickup_times="09:00 - 12:00",
                special_instructions="Near the checkout counter. Ask for Mary.",
                is_available=True,
                giver_id=users[2].id,
                category_id=categories[3].id
            ),
            Item(
                title="Textbooks - Form 1 & 2",
                description="Mathematics, English, Kiswahili books. Still useful.",
                photo_url="https://via.placeholder.com/300?text=Books",
                condition="Fair",
                pickup_location="Kenya Commercial Bank, Roysambu",
                pickup_days="Weekends",
                pickup_times="10:00 - 16:00",
                special_instructions="I'll be outside the bank",
                is_available=True,
                giver_id=users[0].id,
                category_id=categories[4].id
            ),
            Item(
                title="Electric Kettle",
                description="Works perfectly. Just upgraded to a new one.",
                photo_url="https://via.placeholder.com/300?text=Kettle",
                condition="Good",
                pickup_location="Quickmart Donholm",
                pickup_days="Evenings",
                pickup_times="18:00 - 20:00",
                special_instructions="Call me when you're near",
                is_available=True,
                giver_id=users[1].id,
                category_id=categories[2].id
            )
        ]
        
        db.session.add_all(items)
        db.session.commit()
        print(f"✅ Created {len(items)} items")
        
        # Create requests
        requests = [
            Request(
                message="I'm a first-year student at KU and I have no furniture in my hostel. This sofa would really help!",
                status="pending",
                seeker_id=users[2].id,
                item_id=items[0].id
            ),
            Request(
                message="My family was displaced by floods last year and we lost everything. We need kitchen items urgently.",
                status="approved",
                seeker_id=users[0].id,
                item_id=items[1].id
            ),
            Request(
                message="I have a young niece I'm caring for and she needs clothes. These would be perfect.",
                status="pending",
                seeker_id=users[1].id,
                item_id=items[2].id
            ),
            Request(
                message="My neighbor's son just joined Form 1 and needs books. This would help him a lot.",
                status="pending",
                seeker_id=users[2].id,
                item_id=items[3].id
            )
        ]
        
        db.session.add_all(requests)
        db.session.commit()
        print(f"✅ Created {len(requests)} requests")
        
        print("\n" + "="*60)
        print("🎉 DATABASE RESET WITH MVP DATA - COMPLETE")
        print("="*60)
        print("\n📊 SUMMARY:")
        print(f"   Users: {User.query.count()}")
        print(f"   Categories: {Category.query.count()}")
        print(f"   Items: {Item.query.count()}")
        print(f"   Requests: {Request.query.count()}")
        print("="*60)
        
        print("\n🔑 TEST ACCOUNTS:")
        for user in users:
            print(f"   📱 {user.phone_number} (Password: password123) - {user.name}")
        
        print("\n📦 SAMPLE ITEMS:")
        for item in items[:3]:
            print(f"   • {item.title} - {item.pickup_location}")

if __name__ == "__main__":
    reset_database()