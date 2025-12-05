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
                Student
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Course
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {enrollments.map((enrollment, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {enrollment.student_name} (ID: {enrollment.student_id})
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {enrollment.course_title} (ID: {enrollment.course_id})
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    onClick={() => handleRemove(enrollment.student_id, enrollment.course_id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <TrashIcon className="h-5 w-5 inline" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Enrollment Modal */}
      {showModal && (
        <div className="fixed z-10 inset-0 overflow-y-auto">
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true">
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div className="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
              <form onSubmit={handleSubmit}>
                <div>
                  <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                    Enroll Student in Course
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Student
                      </label>
                      <select
                        required
                        value={formData.student_id}
                        onChange={(e) => setFormData({ ...formData, student_id: e.target.value })}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      >
                        <option value="">Select a student</option>
                        {students.map(student => (
                          <option key={student.id} value={student.id}>
                            {student.name} ({student.email})
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Course
                      </label>
                      <select
                        required
                        value={formData.course_id}
                        onChange={(e) => setFormData({ ...formData, course_id: e.target.value })}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      >
                        <option value="">Select a course</option>
                        {courses.map(course => (
                          <option key={course.id} value={course.id}>
                            {course.title}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>
                <div className="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                  <button
                    type="submit"
                    className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-start-2 sm:text-sm"
                  >
                    Enroll
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowModal(false);
                      setFormData({ student_id: '', course_id: '' });
                    }}
                    className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:col-start-1 sm:text-sm"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Enrollments;