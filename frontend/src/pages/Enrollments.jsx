import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { toast } from 'react-hot-toast';
import { PlusIcon, TrashIcon } from '@heroicons/react/24/outline';

const Enrollments = () => {
  const [enrollments, setEnrollments] = useState([]);
  const [students, setStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    student_id: '',
    course_id: '',
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [studentsRes, coursesRes] = await Promise.all([
        api.get('/students/'),
        api.get('/courses/'),
      ]);
      setStudents(studentsRes.data);
      setCourses(coursesRes.data);
      
      // Fetch enrollments for each student
      const enrollmentPromises = studentsRes.data.map(student => 
        api.get(`/enrollments/student/${student.id}`)
      );
      const enrollmentsRes = await Promise.all(enrollmentPromises);
      
      const allEnrollments = [];
      enrollmentsRes.forEach((res, index) => {
        const studentId = studentsRes.data[index].id;
        res.data.forEach(courseId => {
          allEnrollments.push({
            student_id: studentId,
            course_id: courseId,
            student_name: studentsRes.data[index].name,
            course_title: coursesRes.data.find(c => c.id === courseId)?.title || 'Unknown'
          });
        });
      });
      
      setEnrollments(allEnrollments);
    } catch (error) {
      toast.error('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/enrollments/', formData);
      toast.success('Student enrolled successfully');
      setShowModal(false);
      setFormData({ student_id: '', course_id: '' });
      fetchData();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Operation failed');
    }
  };

  const handleRemove = async (studentId, courseId) => {
    if (!window.confirm('Are you sure you want to remove this enrollment?')) return;
    
    try {
      await api.delete('/enrollments/', {
        data: { student_id: studentId, course_id: courseId }
      });
      toast.success('Enrollment removed successfully');
      fetchData();
    } catch (error) {
      toast.error('Failed to remove enrollment');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Enrollments</h1>
        <button
          onClick={() => setShowModal(true)}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          Enroll Student
        </button>
      </div>

      {/* Enrollments Table */}
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
               