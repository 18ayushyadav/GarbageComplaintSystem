"""
Smart Garbage Complaint System — Seed Data Command

Creates realistic dummy complaints for demonstration and testing.

Usage:
    python manage.py seed_data

This will:
1. Create a superuser (admin/admin123) if not exists
2. Create a test user (testuser/test1234) if not exists
3. Generate 12 realistic garbage complaints across Indian cities
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from complaints.models import Complaint
import random


class Command(BaseCommand):
    help = 'Seed the database with realistic dummy complaints for demonstration'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('\n[SEED] Seeding database with dummy data...\n'))

        # ─── Create Superuser (Admin) ─────────────────────────────────────
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@smartgarbage.com',
                'first_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('  [OK] Superuser created: admin / admin123'))
        else:
            self.stdout.write(self.style.WARNING('  [SKIP] Superuser "admin" already exists'))

        # ─── Create Test User ─────────────────────────────────────────────
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'testuser@example.com',
                'first_name': 'Rahul',
                'last_name': 'Sharma',
            }
        )
        if created:
            test_user.set_password('test1234')
            test_user.save()
            self.stdout.write(self.style.SUCCESS('  [OK] Test user created: testuser / test1234'))
        else:
            self.stdout.write(self.style.WARNING('  [SKIP] Test user "testuser" already exists'))

        # ─── Realistic Dummy Complaints ───────────────────────────────────
        complaints_data = [
            {
                'reporter_name': 'Priya Patel',
                'reporter_email': 'priya.patel@gmail.com',
                'reporter_phone': '+91 98765 43210',
                'location_text': 'Near Sector 15 Market, Noida, Uttar Pradesh',
                'google_maps_link': 'https://maps.google.com/?q=28.5855,77.3100',
                'description': 'Large pile of mixed household waste dumped near the market entrance. '
                               'Includes plastic bags, vegetable waste, and broken glass bottles. '
                               'The waste has been accumulating for over a week and is causing a '
                               'severe stench. Stray dogs are scattering the garbage.',
                'status': 'pending',
                'priority': 'high',
                'user': test_user,
            },
            {
                'reporter_name': 'Amit Kumar',
                'reporter_email': 'amit.kumar@yahoo.com',
                'reporter_phone': '+91 99876 54321',
                'location_text': 'MG Road, Near Metro Station, Bengaluru, Karnataka',
                'google_maps_link': 'https://maps.google.com/?q=12.9716,77.5946',
                'description': 'Overflowing garbage bins near the metro station exit. Construction '
                               'debris mixed with household waste is blocking the footpath. Pedestrians '
                               'are forced to walk on the road. This area is a commercial hub and the '
                               'garbage is creating a bad impression on visitors and tourists.',
                'status': 'in_progress',
                'priority': 'critical',
            },
            {
                'reporter_name': 'Sunita Devi',
                'reporter_email': 'sunita.d@gmail.com',
                'reporter_phone': '+91 87654 32109',
                'location_text': 'Lajpat Nagar Central Market, New Delhi',
                'google_maps_link': 'https://maps.google.com/?q=28.5700,77.2400',
                'description': 'Unauthorised garbage dump has formed behind the market shops. '
                               'Vendors are throwing food waste, packaging materials, and plastic '
                               'daily. The drain is choked with solid waste causing waterlogging '
                               'during rains. Mosquito breeding has increased significantly.',
                'status': 'resolved',
                'priority': 'high',
                'admin_remarks': 'Cleanup completed by municipal crew on 15th Oct. Drain cleared. '
                                 'Warning issued to market vendors. Regular collection scheduled.',
            },
            {
                'reporter_name': 'Rajesh Sharma',
                'reporter_email': 'rajesh.sharma@outlook.com',
                'reporter_phone': '',
                'location_text': 'Bandra West, Near Linking Road, Mumbai, Maharashtra',
                'google_maps_link': 'https://maps.google.com/?q=19.0596,72.8295',
                'description': 'Illegal dumping of construction and demolition waste on the roadside. '
                               'The pile includes cement bags, broken tiles, iron rods, and sand. '
                               'This poses a safety hazard especially at night when visibility is low. '
                               'Multiple complaints to BMC have gone unanswered.',
                'status': 'pending',
                'priority': 'critical',
            },
            {
                'reporter_name': 'Meena Kumari',
                'reporter_email': 'meena.k@gmail.com',
                'reporter_phone': '+91 76543 21098',
                'location_text': 'Anna Nagar, Near Bus Stop, Chennai, Tamil Nadu',
                'google_maps_link': 'https://maps.google.com/?q=13.0827,80.2707',
                'description': 'Garbage bin near the bus stop has not been emptied for 5 days. '
                               'Waste is overflowing onto the pavement. The smell is unbearable '
                               'for passengers waiting at the bus stop. Several plastic bags '
                               'have blown onto the road causing traffic safety concerns.',
                'status': 'in_progress',
                'priority': 'medium',
                'admin_remarks': 'Waste collection truck dispatched. Expected cleanup within 24 hours.',
            },
            {
                'reporter_name': 'Vikram Singh',
                'reporter_email': 'vikram.s@rediffmail.com',
                'reporter_phone': '+91 65432 10987',
                'location_text': 'Connaught Place, Block A, New Delhi',
                'google_maps_link': 'https://maps.google.com/?q=28.6315,77.2167',
                'description': 'Multiple garbage bags dumped near the park entrance in CP. '
                               'Food delivery leftovers, disposable cups, and plates are scattered. '
                               'This is a tourist area and the garbage tarnishes Delhi\'s image. '
                               'CCTV installation suggested to identify dumpers.',
                'status': 'pending',
                'priority': 'medium',
            },
            {
                'reporter_name': 'Aisha Begum',
                'reporter_email': 'aisha.b@gmail.com',
                'reporter_phone': '+91 54321 09876',
                'location_text': 'Charminar Area, Near Laad Bazaar, Hyderabad, Telangana',
                'google_maps_link': 'https://maps.google.com/?q=17.3616,78.4747',
                'description': 'Garbage accumulation in the narrow lanes near Charminar. '
                               'Plastic waste and food leftovers from street vendors are not '
                               'being collected regularly. The heritage area needs special '
                               'attention as tourists visit daily. Rat infestation is also observed.',
                'status': 'resolved',
                'priority': 'high',
                'admin_remarks': 'Heritage zone cleanup drive conducted. Daily collection '
                                 'schedule increased to twice a day. Vendor awareness program initiated.',
            },
            {
                'reporter_name': 'Deepak Verma',
                'reporter_email': 'deepak.v@gmail.com',
                'reporter_phone': '+91 43210 98765',
                'location_text': 'Aundh, Near D-Mart, Pune, Maharashtra',
                'google_maps_link': 'https://maps.google.com/?q=18.5583,73.8073',
                'description': 'Large quantity of household E-waste dumped alongside regular garbage. '
                               'Items include old monitors, computer keyboards, phone chargers, and '
                               'batteries. This e-waste needs special handling as it contains heavy '
                               'metals that can contaminate soil and groundwater.',
                'status': 'pending',
                'priority': 'high',
            },
            {
                'reporter_name': 'Kavitha Nair',
                'reporter_email': 'kavitha.n@hotmail.com',
                'reporter_phone': '+91 32109 87654',
                'location_text': 'Koramangala, 5th Block, Bengaluru, Karnataka',
                'google_maps_link': 'https://maps.google.com/?q=12.9352,77.6245',
                'description': 'Vacant plot being used as an illegal garbage dump by nearby '
                               'restaurants and PG accommodations. The waste attracts stray animals '
                               'at night. Residents have complained multiple times. The plot owner '
                               'needs to be notified and the area fenced.',
                'status': 'in_progress',
                'priority': 'medium',
                'admin_remarks': 'Notice issued to plot owner. Cleanup scheduled for next week.',
            },
            {
                'reporter_name': 'Sanjay Gupta',
                'reporter_email': 'sanjay.g@gmail.com',
                'reporter_phone': '+91 21098 76543',
                'location_text': 'Gomti Nagar, Near Wave Mall, Lucknow, Uttar Pradesh',
                'google_maps_link': 'https://maps.google.com/?q=26.8506,80.9490',
                'description': 'Container bins placed by the municipality are overflowing. '
                               'Waste segregation is not being followed — wet and dry waste '
                               'mixed together. The collection frequency needs to be increased '
                               'given the high population density in this area.',
                'status': 'pending',
                'priority': 'low',
            },
            {
                'reporter_name': 'Fatima Sheikh',
                'reporter_email': 'fatima.s@gmail.com',
                'reporter_phone': '+91 10987 65432',
                'location_text': 'Vastrapur Lake, Near ISRO, Ahmedabad, Gujarat',
                'google_maps_link': 'https://maps.google.com/?q=23.0350,72.5293',
                'description': 'Plastic waste found floating in Vastrapur Lake. Visitors '
                               'are throwing plastic bottles, food packets, and wrappers into '
                               'the lake. This is damaging the aquatic ecosystem. Signboards '
                               'and dustbins should be installed at regular intervals.',
                'status': 'resolved',
                'priority': 'critical',
                'admin_remarks': 'Lake cleanup drive completed. 15 dustbins installed around '
                                 'the lake perimeter. Anti-littering signboards placed. Regular '
                                 'patrol assigned.',
            },
            {
                'reporter_name': 'Ravi Teja',
                'reporter_email': 'ravi.t@gmail.com',
                'reporter_phone': '+91 09876 54321',
                'location_text': 'Jubilee Hills, Road No. 36, Hyderabad, Telangana',
                'google_maps_link': 'https://maps.google.com/?q=17.4325,78.4073',
                'description': 'Green waste from tree trimming activities dumped on the roadside. '
                               'Branches, leaves, and trunk pieces are blocking half the road. '
                               'This was left by a private tree-cutting service that did not '
                               'arrange for proper disposal. Causing traffic congestion.',
                'status': 'in_progress',
                'priority': 'medium',
                'admin_remarks': 'Municipal truck dispatched for green waste collection.',
            },
        ]

        created_count = 0
        for data in complaints_data:
            # Check if a similar complaint already exists (by reporter + location)
            if Complaint.objects.filter(
                reporter_email=data['reporter_email'],
                location_text=data['location_text']
            ).exists():
                continue

            complaint = Complaint(
                reporter_name=data['reporter_name'],
                reporter_email=data['reporter_email'],
                reporter_phone=data.get('reporter_phone', ''),
                location_text=data['location_text'],
                google_maps_link=data.get('google_maps_link', ''),
                description=data['description'],
                status=data.get('status', 'pending'),
                priority=data.get('priority', 'medium'),
                admin_remarks=data.get('admin_remarks', ''),
                user=data.get('user', None),
            )
            complaint.save()
            created_count += 1
            self.stdout.write(f'  [+] Created: [{complaint.reference_number}] {complaint.location_text[:50]}')

        self.stdout.write(self.style.SUCCESS(f'\n[OK] Successfully seeded {created_count} complaints!'))
        self.stdout.write(self.style.NOTICE(
            '\nLogin Credentials:'
            '\n   Admin:    username=admin      password=admin123'
            '\n   User:     username=testuser   password=test1234'
            '\n'
        ))
