const fs = require('fs');

let content = fs.readFileSync('src/components/AccountModals.tsx', 'utf8');

// Replace the function signature with types
content = content.replace(
  /export function AccountModals\(\{ activeModal, setActiveModal, userInfo \}\) \{/,
  `type AccountModalsProps = {
  activeModal: string | null;
  setActiveModal: (modal: string | null) => void;
  userInfo?: { name: string; tier: string; is_admin: boolean } | null;
};

export function AccountModals({ activeModal, setActiveModal, userInfo }: AccountModalsProps) {`
);

fs.writeFileSync('src/components/AccountModals.tsx', content);
console.log('Fixed AccountModals types');
