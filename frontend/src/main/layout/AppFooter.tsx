/* eslint-disable @next/next/no-img-element */

import { useLayoutContext } from '../hooks/useLayoutContext';

const AppFooter = () => {
    const { layoutConfig } = useLayoutContext();

    return (
        <div className="layout-footer">
            <img src={`/layout/images/logo-${layoutConfig.colorScheme === 'light' ? 'dark' : 'white'}.svg`} alt="Logo" height="20" className="mr-2" />
            by
            <span className="font-medium ml-2">PrimeReact</span>
        </div>
    );
};

export default AppFooter;
