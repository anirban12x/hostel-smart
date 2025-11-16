from django.core.management.base import BaseCommand
from ACCOUNTS.models import User
from HOSTEL.models import Student


class Command(BaseCommand):
    help = 'Create test users for the hostel management system'

    def handle(self, *args, **options):
        # Create test users
        test_users = [
            {
                'username': 'student1',
                'email': 'student1@test.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'student',
                'password': 'testpass123'
            },
            {
                'username': 'staff1',
                'email': 'staff1@test.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'role': 'staff',
                'password': 'testpass123'
            },
            {
                'username': 'admin1',
                'email': 'admin1@test.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'password': 'testpass123'
            }
        ]

        for user_data in test_users:
            username = user_data['username']
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User {username} already exists, skipping...')
                )
                continue
            
            # Create user
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
            
            # Create student profile if role is student
            if user_data['role'] == 'student':
                try:
                    Student.objects.create(
                        roll_no=f"STU{user.id:03d}",
                        name=f"{user_data['first_name']} {user_data['last_name']}",
                        email=user_data['email'],
                        phone="+1234567890"
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Could not create student profile for {username}: {e}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {user_data["role"]} user: {username}')
            )

        self.stdout.write(
            self.style.SUCCESS('\nTest users created successfully!')
        )
        self.stdout.write('Login credentials:')
        self.stdout.write('- student1 / testpass123 (Student)')
        self.stdout.write('- staff1 / testpass123 (Staff)')  
        self.stdout.write('- admin1 / testpass123 (Admin)')
