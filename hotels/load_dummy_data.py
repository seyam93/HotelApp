
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal
from hotels.models import Hotel, Room, RoomImage, Feature, Specification, Facility, HotelImage, WelcomeMessage
from staff.models import Manager
from events.models import Event
from core.models import Contact , Newsletter, Feedback, PrivacyPolicy, TermsAndConditions, FAQ
from restaurants.models import Restaurant, MenuCategory, MenuItem
from meeting_rooms.models import MeetingRoom

fake = Faker()

def create_dummy_data():
    Hotel.objects.all().delete()

    for i in range(3):
        hotel = Hotel.objects.create(
            name=fake.company() + " Hotel",
            address=fake.address(),
            location=fake.city(),
            description=fake.text(),
        )

        for _ in range(2):
            HotelImage.objects.create(
                hotel=hotel,
                image='hotel_images/sample.jpg',
                caption=fake.sentence()
            )

        WelcomeMessage.objects.create(
            hotel=hotel,
            title="Welcome",
            description="A warm welcome to our hotel",
            message="We’re happy to have you with us."
        )

        facility_types = [f[0] for f in Facility.FACILITY_TYPES]
        for _ in range(3):
            Facility.objects.create(
                hotel=hotel,
                type=random.choice(facility_types),
                name=fake.word().capitalize(),
                description=fake.text()
            )

        for _ in range(2):
            Manager.objects.create(
                hotel=hotel,
                name=fake.name(),
                email=fake.email(),
                phone_number=fake.phone_number(),
                facebook=fake.url(),
                instagram=fake.url(),
                linkedin=fake.url(),
                position="Manager"
            )

        for _ in range(4):
            room = Room.objects.create(
                hotel=hotel,
                name=fake.word().capitalize() + " Room",
                description=fake.text(),
                number_of_beds=random.randint(1, 4),
                area=random.uniform(25.0, 80.0),
                is_suit=random.choice([True, False]),
                price_per_night=Decimal(random.uniform(50.00, 300.00)).quantize(Decimal('0.01')),
                is_available=True
            )
            for _ in range(2):
                RoomImage.objects.create(
                    room=room,
                    image='room_images/sample.jpg',
                    caption=fake.sentence()
                )
            for _ in range(2):
                Feature.objects.create(
                    room=room,
                    name=fake.word(),
                    icon='feature_icons/sample.jpg'
                )
                Specification.objects.create(
                    room=room,
                    name=fake.word(),
                    description=fake.text(),
                    icon='specification_icons/sample.jpg'
                )

        for _ in range(1):
            MeetingRoom.objects.create(
                hotel=hotel,
                name=fake.word().capitalize() + " Hall",
                capacity=random.randint(20, 200),
                area=random.uniform(30.0, 200.0),
                description=fake.text()
            )

        for _ in range(2):
            restaurant = Restaurant.objects.create(
                hotel=hotel,
                name=fake.word().capitalize() + " Restaurant",
                description=fake.text(),
                opening_hours="8 AM - 11 PM"
            )
            for _ in range(2):
                category = MenuCategory.objects.create(
                    restaurant=restaurant,
                    name=fake.word().capitalize(),
                    description=fake.sentence()
                )
                for _ in range(3):
                    MenuItem.objects.create(
                        category=category,
                        name=fake.word().capitalize(),
                        description=fake.sentence(),
                        price=Decimal(random.uniform(5.00, 50.00)).quantize(Decimal('0.01'))
                    )

        Event.objects.create(
            hotel=hotel,
            name=fake.catch_phrase(),
            description=fake.text(),
            venue="Main Hall",
            start_date=datetime.today().date(),
            end_date=datetime.today().date() + timedelta(days=2)
        )

        for _ in range(2):
            FAQ.objects.create(
                hotel=hotel,
                question=fake.sentence(),
                answer=fake.paragraph()
            )
            Contact.objects.create(
                hotel=hotel,
                name=fake.name(),
                email=fake.email(),
                message=fake.paragraph()
            )
            Newsletter.objects.create(
                hotel=hotel,
                email=fake.email()
            )
            Feedback.objects.create(
                hotel=hotel,
                name=fake.name(),
                email=fake.email(),
                message=fake.paragraph()
            )
            PrivacyPolicy.objects.create(
                hotel=hotel,
                title="Privacy Policy",
                content=fake.text()
            )
            TermsAndConditions.objects.create(
                hotel=hotel,
                title="Terms and Conditions",
                content=fake.text()
            )

    print("Dummy data created successfully!")
