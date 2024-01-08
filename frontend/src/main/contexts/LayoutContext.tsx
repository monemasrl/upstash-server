import { LayoutConfig, LayoutState } from '@/types';
import { createContext, useState } from 'react';
type LayoutContextType = {
    sidebarVisible: boolean;
    toggleSidebar: () => void;
    layoutConfig: LayoutConfig;
    setLayoutConfig: (config: LayoutConfig) => void;
    layoutState: LayoutState
    setLayoutState: (state: LayoutState) => void;
    onMenuToggle: () => void;
    showProfileSidebar: () => void;
    isOverlay: () => boolean;
    isDesktop: () => boolean;
};

export const LayoutContext = createContext<LayoutContextType>({} as LayoutContextType);
export const LayoutProvider = ({ children }: { children: React.ReactNode }) => {
    const [layoutConfig, setLayoutConfig] = useState<LayoutConfig>({
        ripple: true,
        inputStyle: 'outlined',
        menuMode: 'static',
        colorScheme: 'light',
        theme: 'lara-light-indigo',
        scale: 14
    });

    const [layoutState, setLayoutState] = useState({
        staticMenuDesktopInactive: false,
        overlayMenuActive: true,
        profileSidebarVisible: true,
        configSidebarVisible: false,
        staticMenuMobileActive: false,
        menuHoverActive: false,
        searchActive: false,
    });

    const onMenuToggle = () => {
        if (isOverlay()) {
            setLayoutState((prevLayoutState) => ({ ...prevLayoutState, overlayMenuActive: !prevLayoutState.overlayMenuActive }));
        }

        if (isDesktop()) {
            setLayoutState((prevLayoutState) => ({ ...prevLayoutState, staticMenuDesktopInactive: !prevLayoutState.staticMenuDesktopInactive }));
        } else {
            setLayoutState((prevLayoutState) => ({ ...prevLayoutState, staticMenuMobileActive: !prevLayoutState.staticMenuMobileActive }));
        }
    };

    const showProfileSidebar = () => {
        setLayoutState((prevLayoutState) => ({ ...prevLayoutState, profileSidebarVisible: !prevLayoutState.profileSidebarVisible }));
    };

    const isOverlay = () => {
        return layoutConfig.menuMode === 'overlay';
    };

    const isDesktop = () => {
        return window.innerWidth > 991;
    };

    return (
    <LayoutContext.Provider
        value={{
            sidebarVisible: false,
            toggleSidebar: () => {
                setLayoutState({
                    ...layoutState,
                    staticMenuMobileActive: !layoutState.staticMenuMobileActive
                });
            },
            layoutConfig,
            setLayoutConfig,
            layoutState,
            setLayoutState,
            onMenuToggle,
            showProfileSidebar,
            isOverlay,
            isDesktop
        }}
    >
        {children}
    </LayoutContext.Provider>
    );
};