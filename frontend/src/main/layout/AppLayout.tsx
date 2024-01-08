import { ChildContainerProps } from "@/types";
import { classNames } from "primereact/utils";
import React from "react";
import { useLayoutContext } from "../hooks/useLayoutContext";
import AppFooter from "./AppFooter";
import AppSidebar from "./AppSidebar";
import AppTopbar from "./AppTopbar";

function AppLayout({ children }: ChildContainerProps) {
    const { layoutConfig, layoutState } = useLayoutContext();

    const containerClass = classNames("layout-wrapper", {
        'layout-overlay': layoutConfig.menuMode === 'overlay',
        'layout-static': layoutConfig.menuMode === 'static',
        'layout-static-inactive': layoutState.staticMenuDesktopInactive && layoutConfig.menuMode === 'static',
        'layout-overlay-active': layoutState.overlayMenuActive,
        'layout-mobile-active': layoutState.staticMenuMobileActive,
        'p-input-filled': layoutConfig.inputStyle === 'filled',
        'p-ripple-disabled': !layoutConfig.ripple
    });

    return (
        <React.Fragment>
            <div className={containerClass}>
                <AppTopbar />
                <div className="layout-sidebar">
                    <AppSidebar />
                </div>
                <div className="layout-main-container">
                    <div className="layout-main">{children}</div>
                    <AppFooter />
                </div>
                <div className="layout-mask"></div>
            </div>
        </React.Fragment>
    );
}

export default AppLayout