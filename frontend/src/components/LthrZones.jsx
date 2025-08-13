import { useState } from "react"

const LthrZones = () => {
  const [lthr, setLthr] = useState("")
  const [zones, setZones] = useState([])

  const calculateZones = () => {
    const L = parseFloat(lthr)
    if (isNaN(L)) return

    const data = [
      {
        name: "Level 1 (L1) – Walking/Jog",
        range: `<${Math.round(L * 0.68)} bpm`,
        detail: "<68% LTHR, 0-2 RPE",
      },
      {
        name: "Level 2 (L2) – Easy pace",
        range: `${Math.round(L * 0.69)}–${Math.round(L * 0.83)} bpm`,
        detail: "69-83% LTHR, 2-3 RPE",
      },
      {
        name: "Level 3 (L3) – Marathon pace",
        range: `${Math.round(L * 0.84)}–${Math.round(L * 0.94)} bpm`,
        detail: "84-94% LTHR, 3-4 RPE",
      },
      {
        name: "Level 4 (L4) – Threshold pace",
        range: `${Math.round(L * 0.95)}–${Math.round(L * 1.05)} bpm`,
        detail: "95-105% LTHR, 4-5 RPE",
      },
      {
        name: "Level 5 (L5) – Interval pace",
        range: `${Math.round(L * 1.06)}+ bpm`,
        detail: "106%< LTHR, 6-7 RPE",
      },
      {
        name: "Level 6 (L6) – Repetition pace",
        range: `${Math.round(L * 1.06)}+ bpm`,
        detail: "106%< LTHR, 7-10 RPE",
      },
      {
        name: "Level 7 (L7) – Max Effort",
        range: "",
        detail: "",
      },
    ]

    setZones(data)
  }

  return (
    <div className="LthrZones">
      <h1>
        Lactate Threshold <br></br>
        Heart Rate Zones
      </h1>
      <div className="card" style={{ marginTop: 16 }}>
        <p className="formatText">Enter Heart Rate Test Result</p>
        <input
          type="number"
          placeholder="Heart Rate"
          value={lthr}
          onChange={(e) => setLthr(e.target.value)}
          style={{ padding: 8, marginRight: 8 }}
        />
        <button onClick={calculateZones}>Estimate</button>
      </div>

      {zones.length > 0 && (
        <div className="fade" style={{ marginTop: 16 }}>
          {zones.map((zone, idx) => (
            <div key={idx} style={{ marginBottom: 12 }}>
              <strong>{zone.name}</strong>
              <div>{zone.range}</div>
              <small>{zone.detail}</small>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default LthrZones
