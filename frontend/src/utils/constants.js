// frontend/src/utils/constants.js
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://school-management-backend.onrender.com';
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'Student Management System';

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  STUDENTS: '/students',
  COURSES: '/courses',
  ENROLLMENTS: '/enrollments',
  PROFILE: '/profile',
};