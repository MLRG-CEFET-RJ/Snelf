import * as React from 'react';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import Logo from '../assets/s_logo.png'
import { FlexContainer } from './ui/flex-container';

const pages = [
    ['Home', '/'], 
    ['Base', '/base'], 
    ['Treinamento', '/training'], 
    ['Medicamentos', '/medicines'], 
    ['Suprimentos', '/supplies'],
    ['Alimentos', '/food'],
    ['Escolares', '/school-products']
];

function ResponsiveAppBar() {
    const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);

    const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElNav(event.currentTarget);
    };

    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };

    return (
        <FlexContainer sx={{ backgroundColor: '#1976D2', color: 'white' }}>
            <Container maxWidth="xl">
                <Toolbar disableGutters>
                    <FlexContainer
                        sx={{
                            display: { xs: 'none', md: 'flex' },
                            justifyContent: 'center'
                        }}
                    >
                        <img src={Logo} alt="logo" width={'20%'} style={{ borderRadius: 100 }} />
                    </FlexContainer>

                    <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
                        <IconButton
                            size="large"
                            onClick={handleOpenNavMenu}
                            color="inherit"
                        >
                            <MenuIcon />
                        </IconButton>
                        <Menu
                            id="menu-appbar"
                            anchorEl={anchorElNav}
                            anchorOrigin={{
                                vertical: 'bottom',
                                horizontal: 'left',
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'left',
                            }}
                            open={Boolean(anchorElNav)}
                            onClose={handleCloseNavMenu}
                            sx={{
                                display: { xs: 'block', md: 'none' },
                            }}
                        >
                            {pages.map((page) => (
                                <MenuItem key={page[0]} onClick={handleCloseNavMenu}>
                                    <Typography textAlign="center">{page[0]}</Typography>
                                </MenuItem>
                            ))}
                        </Menu>
                    </Box>
                    <FlexContainer
                        sx={{
                            display: { xs: 'flex', md: 'none' },
                            flexGrow: 1,
                            justifyContent: 'center'
                        }}
                    >
                        <img src={Logo} alt="logo" width={'5%'} style={{ borderRadius: 100 }} />
                    </FlexContainer>
                    <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
                        {pages.map((page) => (
                            <Button
                                key={page[0]}
                                href={page[1]}
                                sx={{ my: 2, color: 'white', display: 'block' }}
                            >
                                {page[0]}
                            </Button>
                        ))}
                    </Box>
                </Toolbar>
            </Container>
        </FlexContainer>
    );
}
export default ResponsiveAppBar;
