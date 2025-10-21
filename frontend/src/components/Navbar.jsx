import React from 'react';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">SM</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-800">StudyMate</h1>
          </div>
          
          <div className="hidden md:flex items-center space-x-6">
            <span className="text-sm text-gray-600">NCERT Classes 6-10</span>
            <span className="px-4 py-2 bg-indigo-100 text-indigo-600 rounded-lg text-sm font-medium">
              Science • Maths • English
            </span>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
