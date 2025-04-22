from django.core.management.base import BaseCommand
from hotels.models import Hotel, Room, RoomImage, Feature, Specification, Facility
from staff.models import Manager
from events.models import Event
from restaurants.models import Restaurant
from meeting_rooms.models import MeetingRoom
from django.utils.text import slugify
from datetime import date
import random

class Command(BaseCommand):
    help = 'Load full dummy data for all hotels'

    def handle(self, *args, **kwargs):
        if not Hotel.objects.exists():
            self.stdout.write("⚠️  No hotels found. Creating sample hotels...")

            hotel_data = [
                ("Grand Hilton Cairo", "Cairo"),
                ("Blue Moon Resort", "Sharm El Sheikh"),
                ("Alexandria Seaside Inn", "Alexandria"),
                ("Desert Mirage Retreat", "Siwa Oasis"),
                ("Luxe Nile View Hotel", "Luxor"),
                ("Mountain Breeze Lodge", "Saint Catherine"),
                ("Marina Bay Plaza", "North Coast"),
                ("Royal Palm Garden", "Aswan"),
                ("Sunset Valley Hotel", "Hurghada"),
                ("The Pyramid Palace", "Giza"),
            ]

            for name, city in hotel_data:
                Hotel.objects.create(
                    name=name,
                    location=city,
                    address=f"{city} Main Street",
                    description=f"{name} offers top-tier service in {city}.",
                    slug=slugify(name)
                )

            self.stdout.write(f"🏨 Created {len(hotel_data)} sample hotels.")

        hotels = Hotel.objects.all()

        for hotel in hotels:
            # === Rooms ===
            for room_type in ["Standard Room", "Executive Suite"]:
                room = Room.objects.create(
                    hotel=hotel,
                    name=room_type,
                    slug=slugify(f"{hotel.name}-{room_type}-{hotel.id}-{random.randint(100,999)}"),
                    description=f"{room_type} at {hotel.name}.",
                    number_of_beds=1 if room_type == "Standard Room" else 2,
                    area=30 if room_type == "Standard Room" else 60,
                    is_suit=room_type == "Executive Suite",
                    price_per_night=120 if room_type == "Standard Room" else 250,
                    is_available=True,
                    check_in_notes="Check-in after 2 PM",
                    check_out_notes="Check-out before 12 PM",
                    special_check_in_instructions="Bring your ID or passport",
                    children_and_extra_beds_notes="Kids under 6 stay free"
                )

                # Room Images
                RoomImage.objects.create(
                    room=room,
                    image="room_images/placeholder.jpg",
                    caption=f"{room_type} Image"
                )

                # Features
                Feature.objects.create(room=room, name="Free Wi-Fi")
                Feature.objects.create(room=room, name="Air Conditioning")

                # Specifications
                Specification.objects.create(
                    room=room,
                    name="Television",
                    description="42-inch LED TV with cable",
                )
                Specification.objects.create(
                    room=room,
                    name="Minibar",
                    description="Stocked with beverages and snacks",
                )

            # === Facilities ===
            Facility.objects.create(
                hotel=hotel,
                type='spa',
                name="Relaxation Spa",
                description="Unwind with massage & sauna"
            )
            Facility.objects.create(
                hotel=hotel,
                type='gym',
                name="Fitness Center",
                description="Modern cardio & strength equipment"
            )

            # === Manager ===
            Manager.objects.create(
                hotel=hotel,
                name=f"Manager {hotel.name}",
                email=f"manager@{slugify(hotel.name)}.com",
                phone_number="01000000000",
                position="Hotel Manager"
            )

            # === Restaurant ===
            Restaurant.objects.create(
                hotel=hotel,
                name="Main Dining Hall",
                description="Buffet with international cuisine",
                opening_hours="07:00 AM - 11:00 PM"
            )

            # === Meeting Room ===
            MeetingRoom.objects.create(
                hotel=hotel,
                name="Conference Room A",
                description="Projector, AV, AC, Wi-Fi",
                capacity=50
            )

            # === Event ===
            Event.objects.create(
                hotel=hotel,
                name="Welcome Event",
                description="Live music and dinner",
                venue="Conference Room A",
                start_date=date(2025, 5, 10),
                end_date=date(2025, 5, 10),
                is_active=True
            )

        self.stdout.write(self.style.SUCCESS(f"✅ Dummy data loaded for {hotels.count()} hotels."))