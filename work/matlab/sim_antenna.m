% ECE21129 4ECE-B Group 5 antenna simulation (based on the group's corrected script)
diary('sim_antenna.log'); diary on
fprintf('MATLAB %s\n', version);
fc = 10596.25e6;
lambda = physconst('LightSpeed') / fc;
fprintf('fc = %.4f GHz, lambda = %.6f m\n', fc / 1e9, lambda);

obj = reflectorParabolic;
obj.Exciter = dipole;
antennaObject = design(obj, fc);
antennaObject.Radius = 0.9;
antennaObject.FocalLength = 0.63;
antennaObject.Tilt = 90;
disp(antennaObject)
fprintf('FeedOffset = [%g %g %g]\n', antennaObject.FeedOffset);
save('4ECEB_Group5_Antenna.mat', 'antennaObject');
fprintf('Saved 4ECEB_Group5_Antenna.mat\n');

f = figure('Visible', 'off'); show(antennaObject); title('Parabolic reflector antenna geometry');
exportgraphics(f, 'antenna_geometry.png', 'Resolution', 150); close(f);

% Coarse cuts to find the main beam
t = tic;
[Dc, azc, elc] = pattern(antennaObject, fc, -180:2:180, 0);
[~, i] = max(Dc(:)); azGuess = azc(i);
fprintf('Coarse azimuth cut done in %.1f s, peak near az = %g deg\n', toc(t), azGuess);
t = tic;
[De, ~, ele] = pattern(antennaObject, fc, azGuess, -90:2:90);
[~, i] = max(De(:)); elGuess = ele(i);
fprintf('Coarse elevation cut done in %.1f s, peak near el = %g deg\n', toc(t), elGuess);

% Fine grid around the main beam
t = tic;
azF = azGuess - 3:0.02:azGuess + 3;
elF = elGuess - 3:0.02:elGuess + 3;
[D, azG, elG] = pattern(antennaObject, fc, azF, elF);
[Dmax, idx] = max(D(:));
[iEl, iAz] = ind2sub(size(D), idx);
azPeak = azG(iAz); elPeak = elG(iEl);
fprintf('Fine grid done in %.1f s\n', toc(t));
fprintf('RESULT Dmax = %.4f dBi at az = %.2f deg, el = %.2f deg\n', Dmax, azPeak, elPeak);

% Half-power beamwidths in both planes
bwAz = beamwidth(antennaObject, fc, azF, elPeak);
bwEl = beamwidth(antennaObject, fc, azPeak, elF);
fprintf('RESULT HPBW azimuth plane = %.4f deg, elevation plane = %.4f deg\n', bwAz(1), bwEl(1));
save('pattern_results.mat', 'Dmax', 'azPeak', 'elPeak', 'bwAz', 'bwEl', 'D', 'azG', 'elG');

% Full azimuth and elevation cuts for the figures and the map overlay
t = tic;
azCut = -180:0.1:180;
[Dazc, ~, ~] = pattern(antennaObject, fc, azCut, elPeak);
elCut = -180:0.1:180;
[Delc, ~, ~] = pattern(antennaObject, fc, azPeak, elCut);
fprintf('Full cuts done in %.1f s\n', toc(t));
writematrix([azCut(:) Dazc(:)], 'azimuth_cut.csv');
writematrix([elCut(:) Delc(:)], 'elevation_cut.csv');

f = figure('Visible', 'off');
P = polarpattern(azCut, Dazc(:)');
P.TitleTop = sprintf('Azimuth pattern at el = %.2f%s, %.4f GHz', elPeak, char(176), fc / 1e9);
addCursor(P, azPeak);
exportgraphics(f, 'pattern_azimuth.png', 'Resolution', 150); close(f);

f = figure('Visible', 'off');
P = polarpattern(elCut, Delc(:)');
P.TitleTop = sprintf('Elevation pattern at az = %.2f%s, %.4f GHz', azPeak, char(176), fc / 1e9);
addCursor(P, elPeak);
exportgraphics(f, 'pattern_elevation.png', 'Resolution', 150); close(f);

t = tic;
f = figure('Visible', 'off');
pattern(antennaObject, fc, -180:2:180, -90:2:90);
title(sprintf('3D directivity pattern at %.4f GHz', fc / 1e9));
exportgraphics(f, 'pattern_3d.png', 'Resolution', 150); close(f);
fprintf('3D pattern done in %.1f s\n', toc(t));
fprintf('DONE\n');
diary off
