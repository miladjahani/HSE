import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Users, Clock, AlertOctagon, Calendar, AlertTriangle, ShieldAlert, Award } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer, Cell } from 'recharts';

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('/api/dashboard').then(res => setData(res.data)).catch(console.error);
  }, []);

  if (!data) return <div className="flex h-full items-center justify-center text-gray-500 font-bold">در حال بارگذاری داشبورد...</div>;

  const today = new Intl.DateTimeFormat('fa-IR').format(new Date());

  return (
    <div className="space-y-6">
      {/* Old KPIs + New Header KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
         <div className="col-span-2 bg-blue-500 rounded-2xl p-4 text-white flex justify-between items-center shadow-lg transform transition hover:scale-[1.02]">
           <div>
             <div className="text-sm font-semibold opacity-90 mb-1">تاریخ روز</div>
             <div className="text-3xl font-bold">{today}</div>
           </div>
           <Calendar size={40} className="opacity-80" />
         </div>

         <div className="col-span-2 bg-pink-500 rounded-2xl p-4 text-white flex justify-between items-center shadow-lg transform transition hover:scale-[1.02]">
           <div>
             <div className="text-sm font-semibold opacity-90 mb-1">کل پرسنل</div>
             <div className="text-4xl font-bold">{data.total_employees}</div>
           </div>
           <Users size={40} className="opacity-80" />
         </div>

         <div className="col-span-2 bg-teal-400 rounded-2xl p-4 text-white flex justify-between items-center shadow-lg transform transition hover:scale-[1.02]">
           <div>
             <div className="text-sm font-semibold opacity-90 mb-1">نفر-ساعت</div>
             <div className="text-4xl font-bold">{data.man_hours.toLocaleString()}</div>
           </div>
           <Clock size={40} className="opacity-80" />
         </div>

         <div className="col-span-2 bg-amber-400 rounded-2xl p-4 text-white flex justify-between items-center shadow-lg transform transition hover:scale-[1.02]">
           <div>
             <div className="text-sm font-semibold opacity-90 mb-1">روزهای از دست رفته</div>
             <div className="text-4xl font-bold">{data.lost_time_days} روز</div>
           </div>
           <AlertOctagon size={40} className="opacity-80" />
         </div>

         {/* Old KPIs Integration */}
         <div className="col-span-2 bg-white rounded-2xl p-4 border border-gray-100 flex items-center gap-4 shadow-sm">
            <div className="bg-red-100 text-red-600 p-3 rounded-xl"><AlertTriangle size={24} /></div>
            <div>
               <div className="text-xs text-gray-500 font-bold">حوادث باز</div>
               <div className="text-2xl font-bold text-gray-800">{data.open_incidents}</div>
            </div>
         </div>
         <div className="col-span-2 bg-white rounded-2xl p-4 border border-gray-100 flex items-center gap-4 shadow-sm">
            <div className="bg-orange-100 text-orange-600 p-3 rounded-xl"><ShieldAlert size={24} /></div>
            <div>
               <div className="text-xs text-gray-500 font-bold">پرسنل فاقد PPE</div>
               <div className="text-2xl font-bold text-gray-800">{data.missing_ppe}</div>
            </div>
         </div>
         <div className="col-span-2 bg-white rounded-2xl p-4 border border-gray-100 flex items-center gap-4 shadow-sm">
            <div className="bg-yellow-100 text-yellow-600 p-3 rounded-xl"><Calendar size={24} /></div>
            <div>
               <div className="text-xs text-gray-500 font-bold">سررسید طب کار (ماه)</div>
               <div className="text-2xl font-bold text-gray-800">{data.medical_due_soon}</div>
            </div>
         </div>
         <div className="col-span-2 bg-white rounded-2xl p-4 border border-gray-100 flex items-center gap-4 shadow-sm">
            <div className="bg-green-100 text-green-600 p-3 rounded-xl"><Award size={24} /></div>
            <div>
               <div className="text-xs text-gray-500 font-bold">تشویق / تنبیه</div>
               <div className="text-xl font-bold text-gray-800">{data.rewards} / <span className="text-red-500">{data.penalties}</span></div>
            </div>
         </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Left Column: Heinrich & Risk */}
        <div className="space-y-6">
          {/* Heinrich Pyramid */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h3 className="font-bold text-gray-800 mb-6 text-center border-b pb-2">هرم هاینریش (Heinrich Pyramid)</h3>
            <div className="flex flex-col items-center space-y-1 mt-4">
              <div className="w-full flex items-center justify-between text-[#00AEEF] font-bold text-xs">
                <span>نزدیک به حادثه</span>
                <div className="bg-[#00AEEF] text-white w-3/4 py-1 text-center clip-trapezoid">{data.heinrich_pyramid.anomaly_report}</div>
                <span className="w-10"></span>
              </div>
              <div className="w-full flex items-center justify-between text-[#EC008C] font-bold text-xs">
                <span>شبه حادثه</span>
                <div className="bg-[#EC008C] text-white w-2/3 py-1 text-center clip-trapezoid">{data.heinrich_pyramid.near_miss}</div>
                <span className="w-10"></span>
              </div>
              <div className="w-full flex items-center justify-between text-[#00BFA5] font-bold text-xs">
                <span>کمک‌های اولیه</span>
                <div className="bg-[#00BFA5] text-white w-7/12 py-1 text-center clip-trapezoid">{data.heinrich_pyramid.first_aid}</div>
                <span className="w-10"></span>
              </div>
              <div className="w-full flex items-center justify-between text-[#FFB300] font-bold text-xs">
                <span className="text-[10px]">همراه روز از دست رفته</span>
                <div className="bg-[#FFB300] text-white w-5/12 py-1 text-center clip-trapezoid">{data.heinrich_pyramid.lost_time_accident}</div>
                <span className="w-10"></span>
              </div>
              <div className="w-full flex items-center justify-between text-[#6A1B9A] font-bold text-xs">
                <span>فوت</span>
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
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
             <h3 className="font-bold text-gray-800 mb-4 text-center border-b pb-2">ارزیابی ریسک HSE</h3>
             <div className="space-y-4">
                {[
                  { label: 'بحرانی (Critical)', value: data.risk_assessment.critical, color: 'bg-red-600', max: 30 },
                  { label: 'بالا (High)', value: data.risk_assessment.high, color: 'bg-red-500', max: 30 },
                  { label: 'متوسط (Medium)', value: data.risk_assessment.medium, color: 'bg-yellow-400', max: 30 },
                  { label: 'پایین (Low)', value: data.risk_assessment.low, color: 'bg-green-400', max: 30 },
                ].map(item => (
                  <div key={item.label} className="flex items-center text-sm">
                    <span className="w-24 font-semibold text-gray-600 text-left">{item.label}</span>
                    <div className="flex-1 ml-3 relative h-4 bg-gray-100 rounded-full overflow-hidden">
                      <div className={`absolute right-0 top-0 h-full ${item.color} transition-all duration-1000 ease-out`} style={{width: `${Math.min((item.value / item.max) * 100, 100)}%`}}></div>
                    </div>
                    <span className="mr-3 w-6 text-right font-bold text-gray-700">{item.value}</span>
                  </div>
                ))}
             </div>
          </div>
        </div>

        {/* Middle Column: Safety Index Cards */}
        <div className="space-y-4">
           <h3 className="font-bold text-gray-800 text-center mb-2">شاخص‌های ایمنی (Safety Index)</h3>
           <div className="bg-[#00AEEF] rounded-2xl p-5 text-white shadow-lg relative overflow-hidden">
             <div className="font-bold mb-1">ضریب تکرار (Frequency Rate)</div>
             <div className="text-4xl font-bold">{data.frequency_rate}</div>
             <div className="absolute -left-4 -bottom-4 opacity-10"><Activity size={100} /></div>
           </div>
           <div className="bg-[#EC008C] rounded-2xl p-5 text-white shadow-lg relative overflow-hidden">
             <div className="font-bold mb-1">ضریب شدت (Severity Rate)</div>
             <div className="text-4xl font-bold">{data.severity_rate}</div>
             <div className="absolute -left-4 -bottom-4 opacity-10"><Activity size={100} /></div>
           </div>
           <div className="bg-[#00BFA5] rounded-2xl p-5 text-white shadow-lg">
             <div className="font-bold mb-1">مجوزهای کار (Work Permit)</div>
             <div className="text-4xl font-bold">{data.work_permits}</div>
           </div>
           <div className="bg-[#FFB300] rounded-2xl p-5 text-white shadow-lg">
             <div className="font-bold mb-1">آموزش (نفر-ساعت)</div>
             <div className="text-4xl font-bold">{data.training_man_hours}</div>
           </div>
           <div className="bg-[#6A1B9A] rounded-2xl p-5 text-white shadow-lg">
             <div className="font-bold mb-1">مدت زمان بدون حادثه (MBDA)</div>
             <div className="text-4xl font-bold">{data.mbda} روز</div>
           </div>
        </div>

        {/* Right Column: Comparison & Occ Health */}
        <div className="space-y-6">
           <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
              <h3 className="font-bold text-gray-800 mb-4 border-b pb-2">مقایسه شاخص‌های HSE</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between items-center">
                  <span className="w-1/3 font-semibold">Safe-T-Score</span>
                  <span className="font-bold w-12 text-center">{data.comparison.safe_t_score}</span>
                  <div className="flex-1 bg-gray-100 h-4 relative flex items-center justify-center rounded overflow-hidden mr-2">
                     <div className="absolute top-0 right-1/2 h-full bg-[#00AEEF]" style={{width: '20%'}}></div>
                  </div>
                </div>
                {/* Simplified bar chart representation for comparison */}
                <div className="flex justify-between items-center mt-4">
                  <span className="w-1/3 font-semibold text-xs text-left text-gray-500">ضریب شدت 1402</span>
                  <span className="w-12 text-center">{data.comparison.severity_rate_prev}</span>
                  <div className="flex-1 h-3 bg-[#EC008C] opacity-50 rounded-l mr-2" style={{width: '10%'}}></div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="w-1/3 font-semibold text-xs text-left">ضریب شدت امسال</span>
                  <span className="w-12 text-center font-bold">{data.comparison.severity_rate_curr}</span>
                  <div className="flex-1 h-3 bg-[#EC008C] rounded-l mr-2" style={{width: `${data.comparison.severity_rate_curr * 100}%`, minWidth: '2px'}}></div>
                </div>
                <div className="flex justify-between items-center mt-4">
                  <span className="w-1/3 font-semibold text-xs text-left text-gray-500">ضریب تکرار 1402</span>
                  <span className="w-12 text-center">{data.comparison.frequency_rate_prev}</span>
                  <div className="flex-1 h-4 bg-[#FFB300] opacity-50 rounded-l mr-2" style={{width: '80%'}}></div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="w-1/3 font-semibold text-xs text-left">ضریب تکرار امسال</span>
                  <span className="w-12 text-center font-bold">{data.comparison.frequency_rate_curr}</span>
                  <div className="flex-1 h-4 bg-[#6A1B9A] rounded-l mr-2" style={{width: `${(data.comparison.frequency_rate_curr/10)*100}%`}}></div>
                </div>
              </div>
           </div>

           <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
              <h3 className="font-bold text-gray-800 mb-4 border-b pb-2">شاخص‌های بهداشت حرفه‌ای</h3>
              <div className="h-48 w-full relative">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={[
                    {name: 'بیماری شغلی', val: data.occupational_health.disease, color: '#FFB300'},
                    {name: 'افت شنوایی', val: data.occupational_health.hearing_loss, color: '#00BFA5'},
                    {name: 'مشکل تنفسی', val: data.occupational_health.respiratory, color: '#EC008C'},
                    {name: 'کمر درد', val: data.occupational_health.back_pain, color: '#00AEEF'},
                  ]} margin={{top: 20, right: 0, left: 0, bottom: 20}}>
                    <XAxis dataKey="name" tick={{fontSize: 10}} interval={0} />
                    <RechartsTooltip cursor={{fill: '#f5f5f5'}} />
                    <Bar dataKey="val" radius={[4,4,0,0]}>
                      {
                        [0,1,2,3].map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={['#FFB300', '#00BFA5', '#EC008C', '#00AEEF'][index]} />
                        ))
                      }
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
                <div className="absolute top-2 left-2 text-xs font-bold text-gray-500 bg-gray-100 px-2 py-1 rounded">
                  نرخ درگیری: {data.occupational_health.rate}
                </div>
              </div>
           </div>
        </div>

      </div>

      {/* Bottom: Environmental Indicators */}
      <div className="bg-white border border-gray-100 rounded-2xl shadow-sm flex flex-col md:flex-row overflow-hidden items-stretch">
        <div className="bg-[#00BFA5] text-white p-6 flex items-center justify-center w-full md:w-1/5 text-center font-bold text-lg leading-relaxed">
          شاخص‌های<br/>محیط زیستی
        </div>
        <div className="flex-1 p-8 relative">
           {/* Connecting Line */}
           <div className="absolute top-1/2 left-16 right-16 h-1 bg-[#6A1B9A] -mt-0.5 z-0 rounded-full"></div>

           <div className="flex justify-between relative z-10">
              {[
                { val: data.environmental.water_consumption, unit: 'متر مکعب', label: 'مصرف آب', color: 'bg-[#00AEEF]' },
                { val: data.environmental.water_recovery, unit: 'متر مکعب', label: 'بازیافت آب', color: 'bg-[#6A1B9A]' },
                { val: data.environmental.energy_consumption, unit: 'کیلووات', label: 'مصرف برق', color: 'bg-[#00AEEF]' },
                { val: data.environmental.gas_consumption, unit: 'متر مکعب', label: 'مصرف گاز', color: 'bg-[#00BFA5]' },
              ].map((item, idx) => (
                <div key={idx} className="flex flex-col items-center bg-white px-4">
                  <div className="text-xl font-bold mb-4">{item.val.toLocaleString()} <span className="text-sm text-gray-500 font-normal">{item.unit}</span></div>
                  <div className={`w-5 h-5 rounded-full ${item.color} mb-4 shadow-md border-2 border-white ring-2 ring-gray-100`}></div>
                  <div className="text-sm font-semibold text-gray-700">{item.label}</div>
                </div>
              ))}
           </div>
        </div>
      </div>

    </div>
  );
}
