import React from 'react';
import Navbar from '../components/Navbar';
import ChatWindow from '../components/ChatWindow';

const Home = () => {
  return (
    <div className="flex h-screen">
      <Navbar />
      <main className="flex-1 flex items-center justify-center p-4">
        <ChatWindow />
      </main>
    </div>
  );
};

export default Home;
