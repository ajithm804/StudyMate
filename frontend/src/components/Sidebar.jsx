import React from 'react';

const Sidebar = ({ isOpen, onClose }) => {
  const subjects = [
    { name: 'Science', icon: '🔬', color: 'bg-green-500' },
    { name: 'Mathematics', icon: '📐', color: 'bg-blue-500' },
    { name: 'English', icon: '📚', color: 'bg-purple-500' },
  ];

  const classes = ['Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10'];

  if (!isOpen) return null;

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
        onClick={onClose}
      />

      {/* Sidebar */}
      <div className="fixed left-0 top-0 h-full w-64 bg-white shadow-lg z-50 transform transition-transform md:relative md:transform-none">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-800">Subjects</h2>
            <button onClick={onClose} className="md:hidden text-gray-600">
              ✕
            </button>
          </div>

          {/* Subjects */}
          <div className="space-y-3 mb-8">
            {subjects.map((subject) => (
              <div
                key={subject.name}
                className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
              >
                <div className={`w-10 h-10 ${subject.color} rounded-lg flex items-center justify-center text-xl`}>
                  {subject.icon}
                </div>
                <span className="font-medium text-gray-700">{subject.name}</span>
              </div>
            ))}
          </div>

          {/* Classes */}
          <div>
            <h3 className="text-sm font-semibold text-gray-600 mb-3">Classes</h3>
            <div className="space-y-2">
              {classes.map((cls) => (
                <div
                  key={cls}
                  className="px-3 py-2 rounded-lg hover:bg-indigo-50 hover:text-indigo-600 cursor-pointer transition-colors text-gray-700"
                >
                  {cls}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
