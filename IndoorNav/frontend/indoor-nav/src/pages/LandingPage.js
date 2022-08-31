import React from "react";

import ReactDOM from "react-dom";
import { BrowserRouter, Routes, Route, Outlet, Link } from "react-router-dom";
import Navigation from "./Navigation";
import Information from "./Information";


function LandingPage() {
    return (
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="navigation" element={<Navigation></Navigation>} />
          <Route path="information" element={<Information />} />
          <Route path="*" element={<NoPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
    )
  }
  
  function Layout() {
    return (
      <>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/navigation">Navigation</Link>
            </li>
            <li>
              <Link to="/information">Information</Link>
            </li>
          </ul>
        </nav>
  
        <Outlet />
      </>
    )
  }
  
  function Home() {
    return (
      <div>
        <h2>Home</h2>
      </div>
    );
  }
  
  function About() {
    return (
      <div>
        <h2>About</h2>
      </div>
    );
  }
  
  function Dashboard() {
    return (
      <div>
        <h2>Dashboard</h2>
      </div>
    );
  }

  function NoPage() {
    return (
      <div>
        <h2>404 Not Found</h2>
      </div>
    );
  }
  
export default LandingPage;