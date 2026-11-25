v = ver;
fprintf('MATLAB %s\n', version);
fprintf('Antenna Toolbox license: %d\n', license('test', 'Antenna_Toolbox'));
names = {v.Name};
fprintf('Installed: %s\n', strjoin(names, '; '));
fprintf('Cores: %d\n', feature('numcores'));
