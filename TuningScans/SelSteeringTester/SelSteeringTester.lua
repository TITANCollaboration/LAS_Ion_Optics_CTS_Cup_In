--[[
    SelSteeringTester.lua - Scans the target surface and tests the voltages aquired from the steering fits
]]

simion.workbench_program()

-- make a circular array of start positions 
local ycenter = 35         -- center of circle in y
local zcenter = 35         -- center of circle in z
local rad_target = 4       -- radius of circle
local npoints = 33         -- number of points in scan (increment = (2*range)/(n-1)) 33

local excel_enable = 0  -- Use Excel? (1=yes, 0=no)

local ypos        -- present y position
local zpos        -- present z position
local nions       -- number of ions to fly
local data_rec    -- tracks the data to be written to file    

-- ion optics tuning
local ext_energy = 1300     -- voltage on ion target (defines beam energy)
local ext_lens1 = -2500     -- voltage on 3rd extraction electrode (first einzel lens)
local ext_lens2 = 1200      -- voltage on 5th extraction electrode (second einzel lens)
local ext_y = 0             -- voltage on y axis steering of 6th extraction electrode quad (symmetric steering)
local ext_z = 0             -- voltage on z axis steering of 6th extraction electrode quad (symmetric steering)
local bender = 920          -- Bender Voltage
local sel_focus = -1870     -- common voltage on sel for focus
local sel_x = 0             -- voltage on x axis steering of sel (symmetric steering)
local sel_z = 0             -- voltage on z axis steering of sel (symmetric steering)
local fc_deflector = 0      -- faraday cup deflector
local fc_collector = 0      -- faraday cup collector
-- figure out spacing of spots
inc = (2*rad_target)/(npoints-1)

nions = 1    -- adjust number of ions here

-- enter dynamic steering equation coefficients here (copy/paste from python output, thus way more digits than needed haha)
-- Extraction y-axis steering
local c_ey = {}
c_ey[1] = 6996721.94       -- c00
c_ey[2] = -448899.560      -- c01
c_ey[3] = 8505.02820       -- c02
c_ey[4] = -39.7282643      -- c03
c_ey[5] = -628463.664      -- c10
c_ey[6] = 40692.0200       -- c11
c_ey[7] = -785.231198      -- c12
c_ey[8] = 3.87581293       -- c13
c_ey[9] = 18703.0220       -- c20
c_ey[10] = -1218.73795     -- c21
c_ey[11] = 23.8183535      -- c22
c_ey[12] = -0.12188319     -- c23
c_ey[13] = -184.531463     -- c30
c_ey[14] = 12.0735438      -- c31
c_ey[15] = -0.23790606     -- c32
c_ey[16] = 0.00124525      -- c33

-- Extraction z-axis steering
local c_ez = {}
c_ez[1] = 1399990.15       -- c00
c_ez[2] = -98865.7621      -- c01
c_ez[3] = 2281.61602       -- c02
c_ez[4] = -17.0584453      -- c03
c_ez[5] = -91039.8980      -- c10
c_ez[6] = 5999.09117       -- c11
c_ez[7] = -124.496882      -- c12
c_ez[8] = 0.77673451       -- c13
c_ez[9] = 1918.73979       -- c20
c_ez[10] = -113.476615     -- c21
c_ez[11] = 1.89894358      -- c22
c_ez[12] = -0.00618750     -- c23
c_ez[13] = -11.7440177     -- c30
c_ez[14] = 0.52743842      -- c31
c_ez[15] = -0.00227945     -- c32
c_ez[16] = -9.3333e-05      -- c33

-- SEL x-axis steering 
local c_selx ={}
c_selx[1] = 2455939.36
c_selx[2] = -216857.714
c_selx[3] = 6433.95988
c_selx[4] = -63.4768127
c_selx[5] = -211484.774
c_selx[6] =  18721.3048
c_selx[7] = -556.804073
c_selx[8] =  5.50645294
c_selx[9] = 6093.22943
c_selx[10] = -540.001522
c_selx[11] =  16.0784978
c_selx[12] = -0.15918732
c_selx[13] = -58.7987228
c_selx[14] =  5.20939330
c_selx[15] = -0.15507216
c_selx[16] =  0.00153513

-- SEL z-axis steering 
local c_selz = {}
c_selz[1] = 4574830.24
c_selz[2] = -394169.522
c_selz[3] = 11295.4527
c_selz[4] = -107.702526
c_selz[5] = -401899.796 
c_selz[6] = 34582.6416
c_selz[7] = -990.413854
c_selz[8] =  9.44442462
c_selz[9] = 11709.4901
c_selz[10] = -1006.42509
c_selz[11] = 28.8091357
c_selz[12] =  -0.27476515
c_selz[13] = -113.756328
c_selz[14] =  9.76734498
c_selz[15] =-0.27948435
c_selz[16] = 0.00266620

-- Define a function to calculate the steering voltage based on y,z position using 3rd order polynmial surface
function DynamicSteerVoltage_Order3(y, z, c)
  return c[1] + c[2]*z + c[3]*z^2 + c[4]*z^3 + c[5]*y + c[6]*y*z + c[7]*y*z^2 + c[8]*y*z^3 + c[9]*y^2 + c[10]*y^2*z + c[11]*y^2*z^2 + c[12]*y^2*z^3 + c[13]*y^3 + c[14]*y^3*z + c[15]*y^3*z^2 + c[16]*y^3*z^3;
end

function mean(tbl)
    -- Check if the table is empty
    if #tbl == 0 then
        return nil -- If the table is empty, return nil
    end
    
    local sum = 0
    
    -- Calculate the sum of all elements in the table
    for i = 1, #tbl do
        sum = sum + tbl[i]
    end
    
    -- Calculate the mean
    local mean = sum / #tbl
    
    return mean
end

function segment.flym()
  sim_trajectory_image_control = 1 -- don't keep trajectories

file = io.open("data\\IonStartLocationSteering_ke_20_sel_-1870.csv", "w")
--file:write("Generated from IonStartLocation.iob\nYpos,Zpos,ExtElec,Bender,SEL,RFQ,CaptureElec,End")
file:write("Generated from SelSteeringTester.iob\nnumber of ions = "..nions.."\nBender = "..bender.."V\nSEL focus = "..sel_focus.."V\nYpos,Zpos,Sel_x,Sel_z,IonPosition")
  -- Step through all positions
  for i = 1,npoints do
    ypos = ycenter - rad_target + (i-1)*inc
    for j = 1,npoints do
      zpos = zcenter - rad_target + (j-1)*inc
      if ((ypos - ycenter)^2 + (zpos - zcenter)^2)^0.5 <= rad_target
      then
        -- Regenerate particle definitions in case FE cathode properties changed.
        local PL = simion.import 'particlelib.lua'
        PL.reload_fly2('SelSteeringTester.fly2', {
        -- variables to pass to FLY2 file.
        ypos=ypos,
        zpos=zpos,
        nions=nions
        })
		
		-- Adjust voltages based on equation governing 
    ext_y = DynamicSteerVoltage_Order3(ypos,zpos, c_ey)
    ext_z = DynamicSteerVoltage_Order3(ypos,zpos, c_ez)
	sel_x = DynamicSteerVoltage_Order3(ypos,zpos,c_selx)
    sel_z = DynamicSteerVoltage_Order3(ypos,zpos,c_selz)
    -- Set up data recording to file and perform trajectory calculation run.
    data_rec = {ypos,zpos,sel_x,sel_z,nil}
    run()        
      end
    end
  end
  file:close()
end

-- called on start of each run.
local first
local rec_pos1
function segment.initialize_run()
  first = true
  rec_pos1 = -1
end

function segment.fast_adjust()
  -- set extraction optics
  adj_elect1 = ext_energy
  adj_elect2 = 0
  adj_elect3 = ext_lens1
  adj_elect4 = 0
  adj_elect5 = ext_lens2
  -- set extraction steering
  adj_elect6 = -ext_z
  adj_elect7 = -ext_y
  adj_elect8 = ext_z
  adj_elect9 = ext_y
  -- set bender with only a few buttons
  adj_elect10 = bender
  adj_elect20 = -1 * bender
  adj_elect30 = -1 * bender
  adj_elect40 = bender
  -- set SEL steering
  adj_elect101 = sel_focus + sel_z
  adj_elect102 = sel_focus - sel_x
  adj_elect103 = sel_focus - sel_z
  adj_elect104 = sel_focus + sel_x
end


  -- called on every time-step for each particle in PA instance.

splat_dist = {}
function segment.other_actions()
  -- Update the PE surface display on first time-step of run.
  if first 
  then 
    first = false
    sim_update_pe_surface = 1
  end
  -- These if conditionals are checked each time-step on each ion in the run. Very useful for recording individual ion data at some point in the run.
  -- record ion location at faraday cup aperture
  if (ion_py_mm >= 933 and ion_py_mm<= 944.1 and rec_pos1 ~= ion_number and ion_px_mm>=98 and ion_px_mm<=106 and ion_pz_mm>=31.3 and ion_pz_mm<=38.5)
  then
    data_rec[5] = (abs(ion_px_mm - 101.6625)^2 + abs(ion_pz_mm - 35)^2)^0.5
    rec_pos1 = ion_number
  end
  -- Record info when ion splats
  if (ion_splat ~= 0)
  then
    splat_dist[#splat_dist+1] = (abs(ion_px_mm - 101.6625)^2 + abs(ion_pz_mm - 35)^2)^0.5
    file:write('\n',tostring(table.concat(data_rec, ", ")))
  end
end

print(mean(splat_dist))
