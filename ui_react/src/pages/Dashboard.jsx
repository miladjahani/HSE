import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Users, Clock, AlertOctagon, Activity, FileText } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('/api/dashboard').then(res => setData(res.data)).catch(console.error);
  }, []);

  if (!data) return <div>در حال بارگذاری...</div>;

  return (
    <div className="space-y-6">
      {/* Header Date & Top KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
         <div className="bg-[#00AEEF] rounded-lg p-4 text-white flex justify-between items-center shadow-md transform transition hover:scale-105">
           <div>
             <div className="text-sm font-semibold opacity-90">date</div>
             <div className="text-3xl font-bold">1403/12/30</div>
           </div>
           <FileText size={40} className="opacity-80" />
         </div>

         <div className="bg-[#EC008C] rounded-lg p-4 text-white flex justify-between items-center shadow-md transform transition hover:scale-105">
           <div>
             <div className="text-sm font-semibold opacity-90">Total Employees</div>
             <div className="text-4xl font-bold">{data.total_employees}</div>
           </div>
           <Users size={48} className="opacity-80" />
         </div>

         <div className="bg-[#00BFA5] rounded-lg p-4 text-white flex justify-between items-center shadow-md transform transition hover:scale-105">
           <div>
             <div className="text-sm font-semibold opacity-90">Man-hour</div>
             <div className="text-4xl font-bold">{data.man_hours.toLocaleString()}</div>
           </div>
           <Clock size={48} className="opacity-80" />
         </div>

         <div className="bg-[#FFB300] rounded-lg p-4 text-white flex justify-between items-center shadow-md transform transition hover:scale-105">
           <div>
             <div className="text-sm font-semibold opacity-90 uppercase">Lost Time</div>
             <div className="text-4xl font-bold">{data.lost_time_days} Days</div>
           </div>
           <AlertOctagon size={48} className="opacity-80" />
         </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Left Column: Heinrich & Risk */}
        <div className="space-y-6">
          {/* Heinrich Pyramid */}
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
            <h3 className="font-bold text-gray-800 mb-6 text-center border-b pb-2">Heinrich Pyramid</h3>
            <div className="flex flex-col items-center space-y-1 mt-4">
              <div className="w-full flex items-center justify-between text-[#00AEEF] font-bold text-xs">
                <span>Anomaly Report</span>
                <div className="bg-[#00AEEF] text-white w-3/4 py-1 text-center clip-trapezoid">{data.heinrich_pyramid.anomaly_report}</div>
                <span className="w-10"></span>
              </div>
              <div className="w-full flex items-center justify-between text-[#EC008C] font-bold text-xs">
                <span>Near Miss</span>
                <div className="bg-[#EC008C] text-white w-2/3 py-1 text-center clip-trapezoid">{data.heinrich_pyramid.near_miss}</div>
                <span className="w-10"></span>
              </div>
              <div className="w-full flex items-center justify-between text-[#00BFA5] font-bold text-xs">
                <span>First Aid</span>
                <div className="bg-[#00BFA5] text-white w-7/12 py-1 text-center clip-trapezoid">{data.heinrich_pyramid.first_aid}</div>
                <span className="w-10"></span>
              </div>
              <div className="w-full flex items-center justify-between text-[#FFB300] font-bold text-xs">
                <span className="text-[10px]">lost time Accident</span>
                <div className="bg-[#FFB300] text-white w-5/12 py-1 text-center clip-trapezoid">{data.heinrich_pyramid.lost_time_accident}</div>
                <span className="w-10"></span>
              </div>
              <div className="w-full flex items-center justify-between text-[#6A1B9A] font-bold text-xs">
                <span>death</span>
                <div className="bg-[#6A1B9A] text-white w-1/4 py-1 text-center clip-trapezoid">{data.heinrich_pyramid.death}</div>
                <span className="w-10"></span>
              </div>
            </div>
            <style>{`
              .clip-trapezoid { clip-path: polygon(5% 0, 95% 0, 100% 100%, 0% 100%); transition: all 0.3s; }
              .clip-trapezoid:hover { filter: brightness(1.1); transform: scale(1.02); }
            `}</style>
          </div>

          {/* Risk Assessment HSE */}
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
             <h3 className="font-bold text-gray-800 mb-4 text-center border-b pb-2">Risk Assessment HSE</h3>
             <div className="space-y-4">
                {[
                  { label: 'Critical', value: data.risk_assessment.critical, color: 'bg-red-600', max: 30 },
                  { label: 'High', value: data.risk_assessment.high, color: 'bg-red-500', max: 30 },
                  { label: 'Medium', value: data.risk_assessment.medium, color: 'bg-yellow-400', max: 30 },
                  { label: 'Low', value: data.risk_assessment.low, color: 'bg-green-400', max: 30 },
                ].map(item => (
                  <div key={item.label} className="flex items-center text-sm">
                    <span className="w-16 font-semibold text-gray-600">{item.label}</span>
                    <div className="flex-1 ml-2 relative h-4 bg-gray-100">
                      <div className={`absolute left-0 top-0 h-full ${item.color} transition-all duration-1000 ease-out`} style={{width: `${(item.value / item.max) * 100}%`}}></div>
                    </div>
                    <span className="ml-2 w-6 text-right font-bold text-gray-700">{item.value}</span>
                  </div>
                ))}
             </div>
             {/* Simple Axis */}
             <div className="flex justify-between text-xs text-gray-400 mt-2 pl-16 pr-8 border-t pt-1">
               <span>0</span><span>10</span><span>20</span><span>30</span>
             </div>
          </div>
        </div>

        {/* Middle Column: Safety Index Cards */}
        <div className="space-y-4">
           <h3 className="font-bold text-gray-800 text-center mb-2">Safety index</h3>
           <div className="bg-[#00AEEF] rounded p-4 text-white shadow">
             <div className="font-bold mb-1">Frequency Rate</div>
             <div className="text-4xl font-bold">{data.frequency_rate}</div>
           </div>
           <div className="bg-[#EC008C] rounded p-4 text-white shadow">
             <div className="font-bold mb-1">Severity Rate</div>
             <div className="text-4xl font-bold">{data.severity_rate}</div>
           </div>
           <div className="bg-[#00BFA5] rounded p-4 text-white shadow">
             <div className="font-bold mb-1 uppercase">Work Permit</div>
             <div className="text-4xl font-bold">{data.work_permits}</div>
           </div>
           <div className="bg-[#FFB300] rounded p-4 text-white shadow">
             <div className="font-bold mb-1">Training Man-hours</div>
             <div className="text-4xl font-bold">{data.training_man_hours}</div>
           </div>
           <div className="bg-[#6A1B9A] rounded p-4 text-white shadow">
             <div className="font-bold mb-1 uppercase">MBDA</div>
             <div className="text-4xl font-bold">{data.mbda}</div>
           </div>
        </div>

        {/* Right Column: Comparison & Occ Health */}
        <div className="space-y-6">
           <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
              <h3 className="font-bold text-gray-800 mb-4 border-b pb-2">Comparison HSE index</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between items-center">
                  <span className="w-1/3 font-semibold">Safe-T-Score</span>
                  <span className="font-bold">{data.comparison.safe_t_score}</span>
                  <div className="w-1/2 bg-gray-100 h-4 relative flex items-center justify-center">
                     <div className="absolute top-0 right-1/2 h-full bg-[#00AEEF]" style={{width: '20%'}}></div>
                  </div>
                </div>
                {/* Simplified bar chart representation for comparison */}
                <div className="flex justify-between items-center mt-4">
                  <span className="w-1/3 font-semibold text-xs">Severity Rate 1402</span>
                  <div className="w-1/2 h-3 bg-[#EC008C] opacity-50" style={{width: '10%'}}></div>
                  <span className="w-10 text-right">{data.comparison.severity_rate_prev}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="w-1/3 font-semibold text-xs">Severity Rate 1403</span>
                  <div className="w-1/2 h-3 bg-[#EC008C]" style={{width: `${data.comparison.severity_rate_curr * 100}%`, minWidth: '2px'}}></div>
                  <span className="w-10 text-right">{data.comparison.severity_rate_curr}</span>
                </div>
                <div className="flex justify-between items-center mt-4">
                  <span className="w-1/3 font-semibold text-xs">Frequency Rate 1402</span>
                  <div className="w-1/2 h-4 bg-[#FFB300]" style={{width: '80%'}}></div>
                  <span className="w-10 text-right">{data.comparison.frequency_rate_prev}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="w-1/3 font-semibold text-xs">Frequency Rate 1403</span>
                  <div className="w-1/2 h-4 bg-[#6A1B9A]" style={{width: `${(data.comparison.frequency_rate_curr/10)*100}%`}}></div>
                  <span className="w-10 text-right">{data.comparison.frequency_rate_curr}</span>
                </div>
              </div>
           </div>

           <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
              <h3 className="font-bold text-gray-800 mb-4 border-b pb-2">Occupational Health Indicators</h3>
              <div className="h-48 w-full relative">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={[
                    {name: 'rate', val: parseFloat(data.occupational_health.rate), label: data.occupational_health.rate, color: '#FFFFFF'}, // Hidden bar just for scale if needed, or skip
                    {name: 'occupational disease', val: data.occupational_health.disease, color: '#FFB300'},
                    {name: 'hearing loss', val: data.occupational_health.hearing_loss, color: '#00BFA5'},
                    {name: 'Special respiratory', val: data.occupational_health.respiratory, color: '#EC008C'},
                    {name: 'back pain', val: data.occupational_health.back_pain, color: '#00AEEF'},
                  ]} margin={{top: 20, right: 0, left: 0, bottom: 20}}>
                    <XAxis dataKey="name" tick={{fontSize: 9}} interval={0} width={50} />
                    <RechartsTooltip />
                    <Bar dataKey="val">
                      {
                        [0,1,2,3,4].map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={['#fff', '#FFB300', '#00BFA5', '#EC008C', '#00AEEF'][index]} />
                        ))
                      }
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
           </div>
        </div>

      </div>

      {/* Bottom: Environmental Indicators */}
      <div className="bg-white border border-gray-200 rounded-lg shadow-sm flex flex-col md:flex-row overflow-hidden items-stretch">
        <div className="bg-[#00BFA5] text-white p-6 flex items-center justify-center w-full md:w-1/5 text-center font-bold text-lg">
          Environmental<br/>indicators
        </div>
        <div className="flex-1 p-6 relative">
           {/* Connecting Line */}
           <div className="absolute top-1/2 left-10 right-10 h-1 bg-[#6A1B9A] -mt-0.5 z-0"></div>

           <div className="flex justify-between relative z-10">
              {[
                { val: data.environmental.water_consumption, unit: 'm3', label: 'Water Consumption', color: 'bg-[#00AEEF]' },
                { val: data.environmental.water_recovery, unit: 'm3', label: 'Water recovery', color: 'bg-[#6A1B9A]' },
                { val: data.environmental.energy_consumption, unit: 'kwh', label: 'Energy Consumption', color: 'bg-[#00AEEF]' },
                { val: data.environmental.gas_consumption, unit: 'm2', label: 'gas consumption', color: 'bg-[#00BFA5]' },
              ].map((item, idx) => (
                <div key={idx} className="flex flex-col items-center bg-white px-2">
                  <div className="text-xl font-bold mb-4">{item.val.toLocaleString()} {item.unit}</div>
                  <div className={`w-4 h-4 rounded-full ${item.color} mb-4 shadow-md`}></div>
                  <div className="text-xs font-semibold text-gray-600">{item.label}</div>
                </div>
              ))}
           </div>
        </div>
      </div>

    </div>
  );
}
