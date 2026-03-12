import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import HomePage from "./pages/HomePage";
import ItemDetail from "./pages/ItemDetail";
import Profile from "./pages/Profile";
import RequestsPage from "./pages/RequestsPage";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import PostItemForm from "./components/PostItemForm";

function App() {
  return (
    <Router>

      <Navbar />

      <Routes>

        <Route path="/" element={<HomePage />} />

        <Route path="/item/:id" element={<ItemDetail />} />

        <Route path="/post-item" element={<PostItemForm />} />

        <Route path="/profile" element={<Profile />} />

        <Route path="/requests" element={<RequestsPage />} />

        <Route path="/login" element={<Login />} />

        <Route path="/signup" element={<Signup />} />

      </Routes>

    </Router>
  );
}

export default App; 