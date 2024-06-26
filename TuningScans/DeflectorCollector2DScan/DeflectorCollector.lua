--[[
    ExtractionSteering2DScan.lua - scan the intitial ion start position and the extraction steering and record the ion's displacement from the ion axis in the SEL
]]

simion.workbench_program()

-- make a circular array of start positions 
local col_center = 0       -- voltage for extraction y,z steering at center of target
local col_range = 500      -- Range of focus voltages
local nvolts = 20         -- number of voltages in sel focus scan range (increment = (2*range)/(n-1)) 26
local def_center = 500     -- Bender Voltage
local def_range = 500      -- Bender range

local excel_enable = 0  -- Use Excel? (1=yes, 0=no)

local ypos = 35      -- present y position
local zpos = 35      -- present z position
local data_rec       -- tracks the data to be written to file    

-- ion optics tuning
local ext_energy = 1300     -- voltage on ion target (defines beam energy)
local ext_lens1 = -2500     -- voltage on 3rd extraction electrode (first einzel lens)
local ext_lens2 = 1200      -- voltage on 5th extraction electrode (second einzel lens)
local ext_y = 0             -- voltage on y axis steering of 6th extraction electrode quad (symmetric steering)
local ext_z = 0             -- voltage on z axis steering of 6th extraction electrode quad (symmetric steering)
local sel_focus = -1870      -- common voltage on sel for focus
local bender = 920
local collector = 0         -- Collector 
local deflector = 0         -- Deflector 

-- figure out spacing of spots
col_inc = (2*col_range)/(nvolts-1)
def_inc = (2*def_range)/(nvolts-1)

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

-- Define a function to calculate the steering voltage based on y,z position using 3rd order polynmial surface
function DynamicSteerVoltage_Order3(y, z, c)
  return c[1] + c[2]*z + c[3]*z^2 + c[4]*z^3 + c[5]*y + c[6]*y*z + c[7]*y*z^2 + c[8]*y*z^3 + c[9]*y^2 + c[10]*y^2*z + c[11]*y^2*z^2 + c[12]*y^2*z^3 + c[13]*y^3 + c[14]*y^3*z + c[15]*y^3*z^2 + c[16]*y^3*z^3;
end

function mean(table)
    local sum = 0
    local count = 0
    for _, value in ipairs(table) do
        sum = sum + value
        count = count + 1
    end
    if count ~= 0 then
        return sum / count
    else 
        return nil
    end
end

function segment.flym()
    sim_trajectory_image_control = 1 -- don't keep trajectories

    file = io.open("data\\ke_20\\DeflectorCollector_sel"..sel_focus.."_bender"..bender..".csv", "w")
    --file:write("Generated from IonStartLocation.iob\nYpos,Zpos,ExtElec,Bender,SEL,RFQ,CaptureElec,End")
    file:write("Generated from IonStartLocationSteering.iob\nCollector,Deflector,Efficiency,mean distance off axis")

    -- Adjust voltages based on equation governing 
    ext_y = DynamicSteerVoltage_Order3(ypos,zpos, c_ey)
    ext_z = DynamicSteerVoltage_Order3(ypos,zpos, c_ez)
            
    for col = 1,nvolts do
        collector = col_center - col_range + (col-1)*col_inc
        for def = 1,nvolts do
          deflector = def_center - def_range + (def-1)*def_inc
          data_rec = {collector,deflector, nil,nil}
          run()
        end

    end

    file:close()
end

-- called on start of each run.
local first
local rec_pos1
local rec_pos2
local dist_after_deflector
local efficiency
local ion_count
function segment.initialize_run()
  first = true
  rec_pos1 = -1
  rec_pos2 = -1
  dist_after_deflector = {}
  efficiency = 0
  ion_count = 0
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
  adj_elect101 = sel_focus 
  adj_elect102 = sel_focus 
  adj_elect103 = sel_focus 
  adj_elect104 = sel_focus

  -- set faraday cup optics
  adj_elect113 = deflector
  adj_elect114 = collector
end


  -- called on every time-step for each particle in PA instance.
function segment.other_actions()
  -- Update the PE surface display on first time-step of run.
  if first 
  then 
    first = false
    sim_update_pe_surface = 1
  end
  -- These if conditionals are checked each time-step on each ion in the run. Very useful for recording individual ion data at some point in the run.
  -- record ion location at faraday cup deflector
  if (ion_py_mm >= 932 and rec_pos2 ~= ion_number)
  then
    dist_after_deflector[#dist_after_deflector+1] = (abs(ion_px_mm - 101.6625)^2 + abs(ion_pz_mm - 35)^2)^0.5
    efficiency = efficiency + 1
    rec_pos2 = ion_number
  end
end

--Record the data at the end of the run
function segment.terminate_run()
    data_rec[3] = efficiency/ion_count 
    data_rec[4] = mean(dist_after_deflector)
    file:write('\n',tostring(table.concat(data_rec, ", ")))
end

function segment.terminate()
  ion_count = ion_count+1
end