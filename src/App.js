import logo from './logo.svg';
import Home from './Home'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from './Login'
import Register from './Register'

function App() {
  return (
    <BrowserRouter>
    <Routes>
    
      <Route path="/home" element={<Home/>}/> 
        <Route index element={<Login />} />
        <Route path="/register" element={<Register/>} />
    
    </Routes>
  </BrowserRouter>
  );
}

export default App;
