from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact

class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)


class Students(APIView):
    def get(self, request):
        # Define a list with student profiles
        students = [
            {
                "student_id": "102923",
                "name": "Sheryn D. Minahal",
                "program": "Computer Science",
                "year_level": "Sophomore"
            },
            {
                "student_id": "112004",
                "name": "Michael Estacio Pangilinan",
                "program": "Computer Studies Program",
                "year_level": "Sophomore"
            },
            {
                "student_id": "552233",
                "name": "John D. Monyo",
                "program": "Business Administration",
                "year_level": "Senior"
            },
            {
                "student_id": "143256",
                "name": "Celso D. Makatulogsagabi",
                "program": "Electrical Engineering",
                "year_level": "Freshman"
            }
        ]

        # Return the student list as a response
        return Response({"students": students}, status=status.HTTP_200_OK)

class ContactListView(APIView):
    #class helper
    def create_contact(self, data):
        """Helper function to create a Contact object from data."""
        return Contact(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number', ''),
            address=data.get('address', '')
        )
    
    def post(self, request, *args, **kwargs):
        data = request.data  # Can be a single dict or a list of dicts
        
        if isinstance(data, dict):  # Single entry
            contact = self.create_contact(data)
            contact.save()
            return Response({"message": "Contact added successfully!", "id": contact.id}, status=status.HTTP_201_CREATED)

        elif isinstance(data, list):  # Bulk upload
            contacts = [self.create_contact(item) for item in data]
            Contact.objects.bulk_create(contacts)  # Efficient bulk insert
            return Response({"message": f"{len(contacts)} contacts added successfully!"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)


