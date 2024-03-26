--[[
    ExtractionSteering2DScan.lua - scan the intitial ion start position and the Z-axis extraction steering and record the ion's displacement from the ion axis in the SEL
]]

simion.workbench_program()

-- make a circular array of start positions 
local ycenter = 35         -- center of circle in y
local zcenter = 35         -- center of circle in z
local rad_target = 4.9     -- radius of circle
local npoints = 49         -- number of points in one direction of scan
local ext_z_center = 0     -- voltage for extraction y steering at center of target
local ext_z_range = 300    -- one-direction range of extraction y steering (-ext_y_range, ext_y_range)
local nvolts_e = 30        -- number of voltages in extraction steering scan range

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
local sel_focus = -1500     -- common voltage on sel for focus
local sel_x = 0             -- voltage on x axis steering of sel (symmetric steering)
local sel_z = 0             -- voltage on z axis steering of sel (symmetric steering)
local capture_focus = -700  -- focus voltage on capture optics einzel lens
local cap_x = 0             -- voltage on x axis steering of capture quad (symmetric steering)
local cap_z = 0             -- voltage on z axis steering of capture quad (symmetric steering)
local capture_dec = 700     -- top deceleration voltage for thin electrodes (sets to smooth ramp)
local iRFQ = 1300           -- "drift" voltage of RFQ (i.e. nominal MRTOF energy)    

-- figure out spacing of spots
inc = (2*rad_target)/npoints
extz_inc = (2*ext_z_range)/nvolts_e
nions = 1    -- adjust number of ions here

function segment.flym()
  sim_trajectory_image_control = 1 -- don't keep trajectories

file = io.open("data\\ke_20\\IonStartLocationSteering_ke_20.csv", "w")
--file:write("Generated from IonStartLocation.iob\nYpos,Zpos,ExtElec,Bender,SEL,RFQ,CaptureElec,End")
file:write("Generated from IonStartLocationSteering.iob\nnumber of ions = "..nions.."\nBender = "..bender.."V\nSEL focus = "..sel_focus.."V\nCapture focus = "..capture_focus.."V\nDeceleration Top = "..capture_dec.."V\nZpos,Ext_y,Ext_z,IonPosition")
  -- Step through all positions
  for i = 1,npoints+1 do
    zpos = zcenter - rad_target + (i-1)*inc
    -- Regenerate particle definitions in case FE cathode properties changed.
    local PL = simion.import 'particlelib.lua'
    PL.reload_fly2('ExtractionSteeringZaxisScan.fly2', {
    -- variables to pass to FLY2 file.
    ypos=35,
    zpos=zpos,
    nions=nions
    })
    for ext = 1,nvolts_e+1 do
      ext_z = ext_z_center - ext_z_range + (ext-1)*extz_inc
      ext_y = -61*zpos + 2132
      data_rec = {zpos,ext_y,ext_z,nil}
      print('Z pos =', zpos, 'Ext_y =', ext_y, 'Ext_z =', ext_z)
      run()
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
  -- set capture electrode focus
  adj_elect203 = capture_focus
  -- set steering in capure optics to be symmetric
  adj_elect221 = -cap_x
  adj_elect222 = cap_x
  adj_elect223 = -cap_z
  adj_elect224 = cap_z
  -- set same gap for deceleration electrodes since they are connected by resistors
  adj_elect205 = 0
  adj_elect206 = 0.25*capture_dec
  adj_elect207 = 0.5*capture_dec
  adj_elect208 = 0.75*capture_dec
  adj_elect209 = capture_dec
  -- set RFQ input segments to same potential
  adj_elect231 = iRFQ
  adj_elect232 = iRFQ
  adj_elect233 = iRFQ
  adj_elect234 = iRFQ
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
  -- record ion location in center of SEL
  if (ion_py_mm >= 136 and rec_pos1 ~= ion_number)
  then
    data_rec[4] = abs(ion_pz_mm - 35)
    rec_pos1 = ion_number
  end
  -- Record info when ion splats
  if (ion_splat ~= 0)
  then
    file:write('\n',tostring(table.concat(data_rec, ", ")))
  end
end