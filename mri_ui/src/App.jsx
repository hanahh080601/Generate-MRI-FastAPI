import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar/Sidebar";
import "./App.css";
import { appRoutes } from "./routers";

function App() {
    return (
        <BrowserRouter>
            <div className="App">
                <Sidebar />
                <div className="main-content">
                    <Routes>
                        {appRoutes.map((route, index) => {
                            const Page = route.component
                            return <Route key={index} path={route.path} element={<Page />} />
                        })}
                    </Routes>
                </div>
            </div>
        </BrowserRouter>
    );
}

export default App;
