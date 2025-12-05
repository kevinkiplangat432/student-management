# STUDENT MANAGEMENT SYSTEM 

A modern, full-featured Student Management System built with cutting-edge technologies. This system combines the power of React's dynamic frontend with Python's robust backend to deliver a seamless administrative experience for educational institutions.
### Deployment

#### live link here ===>

### Tech stack 
#### Frontend
React 18 - Modern component-based architecture

    ----Tailwind CSS - Utility-first styling with custom components
    
    ----Firebase - Authentication & real-time capabilities
    
    ----React Query - Server state management
    
    ----React Router v6 - Navigation and routing
    
    ----Axios - HTTP client for API calls

#### Backend
    ---FastAPI - High-performance Python web framework
    
    ---PostgreSQL - Relational database with ACID compliance
    
    ---SQLAlchemy 2.0 - ORM with async support
    
    ---Alembic - Database migrations
    
    ---JWT Authentication - Secure token-based auth
    
    ---Pydantic v2 - Data validation and serialization



## Full CRUD Operations
Create - Add new students, courses, enrollments, and academic records

Read - View detailed information with multiple display formats (cards, tables, lists)

Update - Modify existing records with change tracking and version history

Delete - Safe deletion with confirmation prompts and archive options

### Features 
#### Student Management

Student Registration - Add students with comprehensive profiles

Document Upload - Store academic records, IDs, and photos (Firebase Storage)

Real-time Updates - Live student status changes with Firebase listeners

Advanced Filtering - Filter by program, semester, or custom criteria

####  Course & Enrollment

Course Creation - Set up courses with prerequisites and credit hours

Smart Enrollment - Auto-check prerequisites and seat availability

Waitlist System - Automated waitlisting with priority queues

Schedule Conflict Detection - Prevent overlapping course enrollments



### Clone the repository
git clone https://github.com/kevinkiplangat432/student-management.git
#### Navigate to project directory
cd student-management-system

##### Install dependencies
npm install

#### Set up environment variables
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.
### Start the development server
npm run dev

 Environment variables
cp .env.example .env
#### Edit .env with your PostgreSQL and Firebase credentials

#### Database setup
alembic upgrade head

#### Frontend Setup
cd ../frontend
npm install

#### Firebase setup
cp .env.example .env.local
#### Add your Firebase config from Firebase Console

## License and AUthors:
### License
#### MIT LICENSE
Copyright (c) 2024 [Your Name/Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Student Management System"),
to deal in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Authors & Contributors
Lead Developer  kevin kiplangat

github https://github.com/kevinkiplangat432