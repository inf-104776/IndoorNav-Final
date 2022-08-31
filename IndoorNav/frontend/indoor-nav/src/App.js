import './App.css';
import Webcam from './components/WebcamCapture';
import OptionsMenu from './components/OptionsMenu';
import LandingPage from './pages/LandingPage';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <LandingPage></LandingPage>
      </header>
    </div>
  );
}

export default App;
