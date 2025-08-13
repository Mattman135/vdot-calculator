import { useState } from "react"
import "./App.css"
import HMCalculator from "./components/HMCalculator"
import LthrZones from "./components/LthrZones"

function App() {
  const [active, setActive] = useState("hm")

  return (
    <div
      style={{
        maxWidth: 720,
        width: "100%",
        margin: "0 auto",
        display: "flex",
        flexDirection: "column",
        gap: 16,
        padding: 16,
      }}
    >
      <div
        style={{
          display: "flex",
          gap: 8,
          justifyContent: "center",
        }}
      >
        <button onClick={() => setActive("hm")}>
          Half Marathon Calculator
        </button>
        <button onClick={() => setActive("lthr")}>LTHR Calculator</button>
      </div>
      <div style={{ width: "100%" }}>
        {active === "hm" && <HMCalculator />}
        {active === "lthr" && <LthrZones />}
      </div>
    </div>
  )
}

export default App
