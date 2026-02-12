import React, { useState, useEffect, useRef, useCallback } from 'react';
import Webcam from "react-webcam";
import { Client } from "@gradio/client";
import './App.css';

function App() {
  const [mode, setMode] = useState("gallery"); 
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [facingMode, setFacingMode] = useState("environment");
  const [loading, setLoading] = useState(false);
  
  const webcamRef = useRef(null);
  const fileInputRef = useRef(null);

  const runPrediction = async (fileBlob) => {
    setLoading(true);
    try {
      const client = await Client.connect("https://ferdinann-firstaidlens.hf.space/");
      const result = await client.predict("/predict_image", { 
        image_input: fileBlob, 
      });
      setPrediction(result.data[1]); 
    } catch (err) {
      console.error("API Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const captureAndPredict = useCallback(async () => {
    if (mode === "camera" && webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (!imageSrc) return;
      const blob = await fetch(imageSrc).then(r => r.blob());
      runPrediction(blob);
    }
  }, [mode]);

  useEffect(() => {
    let interval;
    if (mode === "camera") {
      interval = setInterval(captureAndPredict, 4000); 
    }
    return () => clearInterval(interval);
  }, [mode, captureAndPredict]);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => setImage(event.target.result);
      reader.readAsDataURL(file);
      runPrediction(file);
    }
  };

  return (
    <div className="min-h-screen bg-white text-slate-800 font-sans flex flex-col selection:bg-red-50">
      <nav className="px-6 py-6 w-full max-w-5xl mx-auto flex justify-center items-center border-b border-slate-50">
        <h1 className="text-[14px] font-black tracking-[0.3em] uppercase border-b-2 border-red-600 pb-0.5">
          FirstAidLens
        </h1>
      </nav>

      <main className="flex-grow w-full max-w-5xl mx-auto px-6 flex items-start justify-center py-4">
        <div className="grid grid-cols-1 lg:grid-cols-[320px_1fr] gap-8 lg:gap-12 items-start w-full">
          
          <section className="space-y-4 w-full max-w-[320px] mx-auto lg:mx-0">
            <div className="space-y-0.5">
              <span className="text-[8px] font-black text-red-500/40 uppercase tracking-widest">Langkah 01</span>
              <h2 className="text-sm font-bold tracking-tight uppercase text-slate-400">{mode === "camera" ? "Scan Visual" : "Upload Visual"}</h2>
            </div>
            
            <div className="relative aspect-square rounded-[2rem] bg-slate-50 overflow-hidden shadow-lg border border-slate-100 group">
              {mode === "camera" ? (
                <>
                  <Webcam audio={false} ref={webcamRef} screenshotFormat="image/jpeg" videoConstraints={{ facingMode: facingMode }} className="w-full h-full object-cover" />
                  <button onClick={() => setFacingMode(p => p === "user" ? "environment" : "user")} className="absolute bottom-3 right-3 bg-white/90 backdrop-blur p-2 rounded-xl shadow-md text-slate-700 active:scale-95 transition-all">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
                  </button>
                </>
              ) : (
                <div onClick={() => fileInputRef.current.click()} className="w-full h-full flex flex-col items-center justify-center cursor-pointer">
                  {image ? <img src={image} className="w-full h-full object-cover" alt="preview" /> : (
                    <div className="text-center space-y-1 opacity-20">
                      <div className="text-2xl font-light">＋</div>
                      <p className="text-[8px] font-black uppercase tracking-widest">Ambil File</p>
                    </div>
                  )}
                </div>
              )}
              <input type="file" ref={fileInputRef} onChange={handleFileUpload} className="hidden" accept="image/*" />
            </div>

            <div className="flex bg-slate-100 p-1 rounded-xl border border-slate-200 shadow-sm">
              <button 
                onClick={() => {setMode("camera"); setPrediction("");}}
                className={`flex-1 py-2 rounded-lg text-[9px] font-black uppercase transition-all ${mode === "camera" ? "bg-white shadow-sm text-red-600" : "text-slate-400"}`}
              >Kamera</button>
              <button 
                onClick={() => {setMode("gallery"); setPrediction(""); setImage(null);}}
                className={`flex-1 py-2 rounded-lg text-[9px] font-black uppercase transition-all ${mode === "gallery" ? "bg-white shadow-sm text-red-600" : "text-slate-400"}`}
              >Galeri</button>
            </div>
          </section>

          <section className="flex flex-col pt-2">
            {loading && !prediction ? (
              <div className="space-y-4 animate-pulse">
                <div className="h-1 w-12 bg-slate-100 rounded"></div>
                <div className="h-8 w-1/2 bg-slate-50 rounded-lg"></div>
                <div className="space-y-2">
                  <div className="h-3 w-full bg-slate-50 rounded"></div>
                  <div className="h-3 w-4/5 bg-slate-50 rounded"></div>
                </div>
              </div>
            ) : prediction ? (
              <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-700">
                <div className="space-y-1">
                  <span className="text-[8px] font-black text-red-500/40 uppercase tracking-widest">Langkah 02</span>
                  <h2 className="text-sm font-bold tracking-tight uppercase text-slate-400">Analisis Diagnosa AI</h2>
                </div>
                
                <div className="bg-slate-50/50 rounded-3xl p-6 border border-slate-100">
                  <div className="text-slate-900 whitespace-pre-line leading-relaxed text-sm">
                    <p className="font-medium text-slate-600 italic border-l-4 border-red-500 pl-4">
                      {prediction.replace(/###|#|\*\*|\-\-\-/g, '')}
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full min-h-[200px] flex flex-col items-center justify-center border-2 border-dashed border-slate-50 rounded-[2rem] opacity-20">
                <p className="text-[9px] font-black uppercase tracking-[0.4em]">Menunggu Visual...</p>
              </div>
            )}
          </section>
        </div>
      </main>

      <footer className="w-full py-8 text-center mt-auto opacity-20">
        <p className="text-[7px] font-black uppercase tracking-[0.4em]">
          2026 FirstAidLens - Create By Ferdinan
        </p>
      </footer>
    </div>
  );
}

export default App;