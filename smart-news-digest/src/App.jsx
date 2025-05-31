import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Feed from './pages/Feed';
import Profile2 from './pages/Profile2';
import Login from './pages/Login'
import SignUp from './pages/SignUp'
import InterestSelector from "./components/InterestDropdown";
import TermsAndConditions from './pages/TermsAndConditions';



function LayoutWrapper() {
  const location = useLocation();
  const hideNavbarOn = ['/profile2']; 
  const shouldHideNavbar = hideNavbarOn.includes(location.pathname);

  return (
    <>
      {!shouldHideNavbar && <Navbar />}
      <Routes>
        <Route path="/feed" element={<Feed />} />
                <Route path="/profile2" element={<Profile2 />} />
                <Route path="/login" element ={<Login />} />
                <Route path="/signup" element = {<SignUp />} />
                <Route path="/terms" element = {<TermsAndConditions />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <Router>
      <LayoutWrapper />
    </Router>
  );
}