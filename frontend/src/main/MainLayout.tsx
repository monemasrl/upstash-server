import { PrimeReactProvider } from 'primereact/api';
import { LayoutProvider } from './contexts/LayoutContext';
import AppLayout from './layout/AppLayout';

function MainLayout({ children }: { children: React.ReactNode}) {
    return (
        <PrimeReactProvider>
            <LayoutProvider>
                <AppLayout>
                    {children}
                </AppLayout>
            </LayoutProvider>
        </PrimeReactProvider>
    );
}

export default MainLayout;