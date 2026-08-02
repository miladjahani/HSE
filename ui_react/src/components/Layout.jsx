import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users, AlertTriangle, Package, PackageOpen, GraduationCap, Stethoscope, Award, FileText, Database, Shield, Leaf, Clock, FileBadge, HardHat } from 'lucide-react';


const MENU_ITEMS = [
  { id: 'dashboard', icon: LayoutDashboard, label: 'داشبورد', path: '/' },
  { id: 'personnel', icon: Users, label: 'پرسنل', path: '/personnel' },
  { id: 'personnel_profile', icon: Shield, label: 'پرونده جامع پرسنل', path: '/profile' },
  { id: 'incidents', icon: AlertTriangle, label: 'حوادث و شبه‌حوادث', path: '/incidents' },
  { id: 'man_hours', icon: Clock, label: 'نفر-ساعت', path: '/man-hours' },
  { id: 'work_permits', icon: FileBadge, label: 'مجوزهای کار', path: '/work-permits' },
  { id: 'environmental', icon: Leaf, label: 'محیط زیست', path: '/environmental' },
  { id: 'ppe_stock', icon: Package, label: 'انبار PPE', path: '/ppe-stock' },
  { id: 'ppe_issuance', icon: PackageOpen, label: 'تحویل PPE', path: '/ppe-issuance' },
  { id: 'training', icon: GraduationCap, label: 'دوره‌های آموزشی', path: '/training' },
  { id: 'medical', icon: Stethoscope, label: 'طب کار', path: '/medical' },
  { id: 'disciplinary', icon: Award, label: 'تشویق و تنبیه', path: '/disciplinary' },
  { id: 'reports', icon: FileText, label: 'گزارش‌گیری', path: '/reports' },
  { id: 'backup', icon: Database, label: 'پشتیبان‌گیری', path: '/backup' },
];

export default function Layout({ children, workspace }) {
  return (
    <div className="flex h-screen overflow-hidden bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-[#151b23] text-gray-300 shadow-xl z-20 flex flex-col transition-all duration-300 ease-in-out">
        <div className="h-16 flex items-center justify-center border-b border-gray-700 p-4 gap-3">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C7.58172 2 4 5.58172 4 10V14C4 15.1046 4.89543 16 6 16H18C19.1046 16 20 15.1046 20 14V10C20 5.58172 16.4183 2 12 2Z" fill="#E74C3C"/>
            <path d="M2 16C2 14.8954 2.89543 14 4 14H20C21.1046 14 22 14.8954 22 16C22 17.1046 21.1046 18 20 18H4C2.89543 18 2 17.1046 2 16Z" fill="#C0392B"/>
            <rect x="11" y="4" width="2" height="6" rx="1" fill="#FFFFFF" fillOpacity="0.3"/>
          </svg>
          <h1 className="text-brand font-bold text-center leading-tight">
            سامانه یکپارچه HSE<br/><span className="text-xs text-gray-400">{workspace?.mine_name}</span>
          </h1>
        </div>

        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="space-y-1">
            {MENU_ITEMS.map((item) => (
              <li key={item.id}>
                <NavLink
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center px-6 py-3 hover:bg-[#1f2937] hover:text-white transition-colors border-r-4 ${
                      isActive ? 'bg-gradient-to-l from-[#1f2937] to-transparent text-brand border-brand font-bold' : 'border-transparent'
                    }`
                  }
                >
                  <item.icon className="w-5 h-5 ml-3" />
                  <span>{item.label}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        <div className="p-4 border-t border-gray-700 text-xs text-center text-gray-500">
          نسخه 2.0.0
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-14 bg-white/80 backdrop-blur-md border-b border-gray-100 flex items-center px-6 shadow-sm z-10">
           <h2 className="text-lg font-semibold text-gray-700">شرکت: {workspace?.company_name}</h2>
        </header>
        <div className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
          {children}
        </div>
      </main>
    </div>
  );
}
