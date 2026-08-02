import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users, AlertTriangle, Package, PackageOpen, GraduationCap, Stethoscope, Award, FileText, Database, Shield } from 'lucide-react';

const MENU_ITEMS = [
  { id: 'dashboard', icon: LayoutDashboard, label: 'داشبورد', path: '/' },
  { id: 'personnel', icon: Users, label: 'پرسنل', path: '/personnel' },
  { id: 'personnel_profile', icon: Shield, label: 'پرونده جامع پرسنل', path: '/profile' },
  { id: 'incidents', icon: AlertTriangle, label: 'حوادث و شبه‌حوادث', path: '/incidents' },
  { id: 'ppe_stock', icon: Package, label: 'انبار PPE', path: '/ppe-stock' },
  { id: 'ppe_issuance', icon: PackageOpen, label: 'تحویل PPE', path: '/ppe-issuance' },
  { id: 'training', icon: GraduationCap, label: 'دوره‌های آموزشی', path: '/training' },
  { id: 'medical', icon: Stethoscope, label: 'طب کار', path: '/medical' },
  { id: 'disciplinary', icon: Award, label: 'تشویق و تنبیه', path: '/disciplinary' },
  { id: 'reports', icon: FileText, label: 'گزارش‌گیری و خروجی', path: '/reports' },
  { id: 'backup', icon: Database, label: 'پشتیبان‌گیری', path: '/backup' },
];

export default function Layout({ children, workspace }) {
  return (
    <div className="flex h-screen overflow-hidden bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-sidebar text-gray-300 flex flex-col transition-all duration-300 ease-in-out">
        <div className="h-16 flex items-center justify-center border-b border-gray-700 p-4">
          <h1 className="text-brand font-bold text-center leading-tight">
            سامانه یکپارچه مدیریت HSE<br/>{workspace?.mine_name}
          </h1>
        </div>

        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="space-y-1">
            {MENU_ITEMS.map((item) => (
              <li key={item.id}>
                <NavLink
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center px-6 py-3 hover:bg-gray-800 hover:text-white transition-colors border-r-4 ${
                      isActive ? 'bg-gray-800 text-brand border-brand font-bold' : 'border-transparent'
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
        <header className="h-14 bg-white border-b border-gray-200 flex items-center px-6 shadow-sm z-10">
           <h2 className="text-lg font-semibold text-gray-700">شرکت: {workspace?.company_name}</h2>
        </header>
        <div className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
          {children}
        </div>
      </main>
    </div>
  );
}
