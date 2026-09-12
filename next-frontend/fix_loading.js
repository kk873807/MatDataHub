const fs = require('fs');

// 1. Fix TopNav.tsx
let topnav = fs.readFileSync('src/components/TopNav.tsx', 'utf8');
topnav = topnav.replace(
  /const \[userInfo, setUserInfo\] = useState<\{ name: string; tier: string; is_admin: boolean \} \| null>\(null\);/g,
  'const [userInfo, setUserInfo] = useState<any>(null);'
);
topnav = topnav.replace(
  /if \(data\) setUserInfo\(\{ name: data.name \|\| data.email, tier: data.tier, is_admin: data.is_admin \|\| false \}\);/g,
  'if (data) { data.name = data.name || data.email; setUserInfo(data); }'
);
fs.writeFileSync('src/components/TopNav.tsx', topnav);
console.log('Fixed TopNav.tsx');

// 2. Fix AccountModals.tsx
let modals = fs.readFileSync('src/components/AccountModals.tsx', 'utf8');

// Replace the initial state
modals = modals.replace(
  /const \[profile, setProfile\] = useState<any>\(null\);/g,
  'const [profile, setProfile] = useState<any>(userInfo || null);'
);

// Replace the useEffect that fetches on activeModal change
const oldEffect = `  useEffect(() => {
    if (activeModal) {
      fetchProfile();
    }
  }, [activeModal]);`;

const newEffect = `  useEffect(() => {
    if (userInfo) {
      setProfile(userInfo);
    }
  }, [userInfo]);`;
modals = modals.replace(oldEffect, newEffect);

fs.writeFileSync('src/components/AccountModals.tsx', modals);
console.log('Fixed AccountModals.tsx loading');
