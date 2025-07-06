import React, { useState } from 'react';
import { Route, Routes, Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Login from './Login';
import Register from './Register';
import History from './History';
import Home from './Home';
import Product from './Product';
import Solution from './Solution';
import Resource from './Resource';
import Pricing from './Pricing';
import Search from './Search';
import CreatePlan from './CreatePlan'; // Import CreatePlan component
import Navbar from './Navbar'; // Import Navbar

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [email, setEmail] = useState(null);
    const navigate = useNavigate();

    const handleLogin = async (email, password) => {
        try {
            const response = await axios.post('http://localhost:5000/api/auth/login', { email, password });
            if (response.status === 200) {
                setIsAuthenticated(true);
                setEmail(email); // Store the email
                navigate('/search'); // Navigate to the search page after login
            }
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    const handleRegister = async (name, email, password) => {
        try {
            const response = await axios.post('http://localhost:5000/api/auth/register', { name, email, password });
            if (response.status === 200) {
                setIsAuthenticated(true);
                setEmail(email); // Store the email
                navigate('/search'); // Navigate to the search page after registration
            }
        } catch (error) {
            console.error('Registration failed:', error);
        }
    };

    const handleLogout = () => {
        setIsAuthenticated(false);
        setEmail(null);
        navigate('/'); // Navigate to the home page after logout
    };

    return (
        <div className="container mt-5">
            <Navbar isAuthenticated={isAuthenticated} handleLogout={handleLogout} /> {/* Pass props to Navbar */}
            <Routes>
                <Route path="/login" element={<Login onLogin={handleLogin} />} />
                <Route path="/register" element={<Register onRegister={handleRegister} />} />
                <Route path="/history" element={isAuthenticated ? <History email={email} /> : <Navigate to="/login" />} />
                <Route path="/product" element={<Product />} />
                <Route path="/solution" element={<Solution />} />
                <Route path="/resource" element={<Resource />} />
                <Route path="/pricing" element={<Pricing />} />
                <Route path="/" element={<Home isAuthenticated={isAuthenticated} />} /> {/* Pass isAuthenticated to Home */}
                <Route path="/search" element={isAuthenticated ? <Search email={email} /> : <Navigate to="/login" />} />
                <Route path="/create-plan" element={isAuthenticated ? <CreatePlan email={email} /> : <Navigate to="/login" />} /> {/* Add route for CreatePlan */}
            </Routes>
        </div>
    );
}

export default App;