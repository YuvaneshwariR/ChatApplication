**Project Overview**
This is a Django-based web application designed to provide real-time messaging features similar to popular messaging platforms. 
The application includes functionalities like user authentication, friend requests, and a chat system. 
This README provides an overview of the project, design choices, setup instructions, and potential next steps for further development.

**Features**
User Authentication
Registration
Login
Logout
**Friend Requests**
Send Friend Request
Accept/Reject Friend Request
**Chat System**
One-on-one Chat
Real-time Messaging
Dashboard
View Friends List
View Incoming Friend Requests

## Incomplete Aspects and Potential Next Steps

### Frontend Framework
- **Current Implementation**: The current implementation uses Bootstrap, HTML, and CSS for the frontend. This choice was made to quickly prototype the application and focus on core functionality.
- **Reasoning**: The use of Bootstrap, HTML, and CSS was chosen due to the developer's current expertise in these technologies. These tools allowed for the rapid development of the application's user interface.
- **Recommended Next Step**: Given more time and additional resources, the frontend could be refactored to use React. React offers a more robust and scalable solution for building interactive user interfaces, and it would be beneficial for handling the dynamic nature of the chat application. However, this would require learning React or collaborating with a developer who has experience with it.




**Design Choices**

Simple and Clean UI: Focused on a user-friendly and straightforward interface.
Real-time Chat: Implemented using AJAX for real-time message updates.
Separation of Concerns: Used Django’s views, models, and templates effectively to separate logic, data, and presentation layers.
**Assumptions**
Users must be authenticated to use the chat features.
The application assumes a simple one-on-one messaging system.
Friend request acceptance is required before messaging can occur between users.
**Setup Instructions**
Prerequisites
Python 3.8+
Django 3.2+
PostgreSQL or SQLite (for development)

**Installation Steps**
Clone the Repository:
Copy code
git clone https://github.com/YuvabeshwariR/chat_application.git
cd chat_application

**Create and Activate Virtual Environment:**
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

**Install Dependencies:**
pip install -r requirements.txt

**Database Setup:**
Configure your database settings in chat_application/settings.py.
Run migrations:
python manage.py migrate

**Create Superuser:**
python manage.py createsuperuser

**Run the Development Server:**
python manage.py runserver

**Access the Application:**
Open your web browser and navigate to http://127.0.0.1:8000.

########################################################################################################################

**Incomplete Aspects**
  Some features might be partially implemented or not fully tested.
  Error handling and edge cases might need more robust solutions.

**Potential Next Steps**

**1. Group Chat**
  Description: Enable users to create and participate in group chats.
  Implementation:
    Create a Group model and a GroupMessage model.
    Update views and templates to support group messaging.
**2. Block User**
    Description: Allow users to block other users from sending them messages.
    Implementation:
        Create a BlockedUser model.
        Add views and template logic to handle blocking and unblocking users.
**3. Seen / Delivery Status**
    Description: Show delivery and seen status for messages.
    Implementation:
      Add delivered and seen fields to the Message model.
      Update views to manage and display these statuses.
**4. Error Handling for Multiple Scenarios**
    Description: Implement comprehensive error handling.
    Implementation:
      Add try-except blocks in views.
      Display error messages in templates.
      Implement client-side validation.

Instructions for Developers
Branching Strategy: Use feature branches for new developments.
Code Review: Ensure code is peer-reviewed before merging to the main branch.
Testing: Write unit tests for new features and ensure they pass before deployment.

