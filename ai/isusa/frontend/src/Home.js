import React from 'react';

function Home({ isAuthenticated }) {
    return (
        <div className="container mt-5">
            <h2>Welcome to the Home Page</h2>
            {isAuthenticated && <p>You are logged in!</p>}
        </div>
    );
}

export default Home;