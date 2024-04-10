--[[
    ExtractionSteering2DScan.lua - scan the intitial ion start position and the extraction steering and record the ion's displacement from the ion axis in the SEL
]]

simion.workbench_program()

local electrode1_center = 0  -- voltage for extraction y,z steering at center of target
local electrode1_range = 100      -- Range of focus voltages

local electrode2_center = 920     -- voltage for extraction y,z steering at center of target
local electrode2_range = 100      -- Range of focus voltages

local nvolts = 20         -- number of voltages in focus scan range (increment = (2*range)/(n-1)) 26

local data_rec       -- tracks the data to be written to file    

-- ion optics tuning 
local ext_energy = 1300     -- voltage on ion target (defines beam energy)
local ext_lens1 = 800     -- voltage on 3rd extraction electrode (first einzel lens)       tune1: -2850 tune 2: 800
local ext_lens2 = 875      -- voltage on 5th extraction electrode (second einzel lens)      tune1: 1600  tune 2: 875                
local ext_y = 0             -- voltage on y axis steering of 6th extraction electrode quad (symmetric steering) 
local ext_z = 0             -- voltage on z axis steering of 6th extraction electrode quad (symmetric steering)
local bender = 920          -- Bender Voltage
local sel_focus = -1850     -- common voltage on sel for focus tune 1: -1525 tune 2: -1850

set_electrodes = {ext_energy, ext_lens1, ext_lens2, ext_y,ext_z,bender,sel_focus} -- array used to update electrodes
electrode_names = {"extEnergy", "extLens1", "extLens2", "extYsteer", "extZsteer", "bender", "selFocus"}

local electrode1 -- stores the value of the voltage on the first scanned electrode
local electrode2 -- stores the value of the voltage on the second scanned electrode

ielectrode1 = 5 -- index of the first electrode to be used in the scan
ielectrode2 = 6 -- index of the second electrode to be used in the scan

-- figure out spacing of spots
lens1_inc = (2*electrode1_range)/(nvolts-1)
lens2_inc = (2*electrode2_range)/(nvolts-1)

function mean(table)
  if table ~= nil
  then
    local sum = 0
    local count = 0
    for _, value in ipairs(table) do
        sum = sum + value
        count = count + 1
    end
    return sum / count
  else
    return nil
  end
end

function max(table)
  local largest = nil
  if table~=nil
  then
    for key, value in pairs(table) do
        if largest == nil or value > largest then
            largest = value
        end
    end
    return largest
  else 
    return nil
  end
end

function min(table)
  local smallest = nil
  if table~=nil
  then
    for key, value in pairs(table) do
        if smallest == nil or value < smallest then
            smallest = value
        end
    end
    return smallest
  else 
    return nil
  end
end


function segment.flym()
    sim_trajectory_image_control = 1 -- don't keep trajectories

    file = io.open("data\\ke_20\\2DElectrodeScan_"..electrode_names[ielectrode1].."_"..electrode_names[ielectrode2].."_ke_20_centered_"..electrode1_center.."_"..electrode2_center.."_nvolts_"..nvolts..".csv", "w")
    file:write("Generated from 2DFullTargetScan.iob\n"..electrode_names[ielectrode1]..", "..electrode_names[ielectrode2]..",Efficiency, Mean dist, Median dist, Max dist, Min dist")
            
    for v1 = 1,nvolts do
        electrode1 = electrode1_center - electrode1_range + (v1-1)*lens1_inc
        for v2 = 1, nvolts do 
          electrode2 = electrode2_center - electrode2_range + (v2-1)*lens2_inc
          
          set_electrodes[ielectrode1] = electrode1
          set_electrodes[ielectrode2] = electrode2

          data_rec = {electrode1,electrode2,nil,nil,nil, nil,nil}
          print(electrode_names[ielectrode1]..": " ..electrode1.. "    "..electrode_names[ielectrode2]..": "..electrode2)
          run()
        end 
    end

    file:close()
end

-- called on start of each run.
local first
local rec_pos
local dist
local efficiency
local ion_count
function segment.initialize_run()
  first = true
  rec_pos = -1
  dist = {}
  efficiency = 0
  ion_count = 0
end

function segment.fast_adjust()
  -- set extraction optics
  adj_elect1 = set_electrodes[1]
  adj_elect2 = 0
  adj_elect3 = set_electrodes[2]
  adj_elect4 = 0
  adj_elect5 = set_electrodes[3]
  -- set extraction steering
  adj_elect6 = -set_electrodes[5]
  adj_elect7 = -set_electrodes[4]
  adj_elect8 = set_electrodes[5]
  adj_elect9 = set_electrodes[4]
  -- set bender with only a few buttons
  adj_elect10 = set_electrodes[6]
  adj_elect20 = -1 * set_electrodes[6]
  adj_elect30 = -1 * set_electrodes[6]
  adj_elect40 = set_electrodes[6]
  -- set SEL steering
  adj_elect101 = set_electrodes[7] 
  adj_elect102 = set_electrodes[7] 
  adj_elect103 = set_electrodes[7] 
  adj_elect104 = set_electrodes[7]
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

  if (ion_py_mm >= 323 and ion_px_mm<= 104.5 and ion_px_mm>= 98.5 and ion_pz_mm<=38 and ion_pz_mm>=32 and rec_pos ~= ion_number)
  then
    dist[#dist+1] = (abs(ion_px_mm - 101.625)^2 + abs(ion_pz_mm - 35)^2)^0.5
    efficiency = efficiency + 1
    rec_pos = ion_number
  end
end

--Record the data at the end of the run
function segment.terminate_run()
    table.sort(dist)
    data_rec[3] = efficiency/ion_count 
    data_rec[4] = mean(dist)
    data_rec[5] = dist[ math.floor(#dist / 2) + 1]
    data_rec[6] = max(dist)
    data_rec[7] = min(dist)

    file:write('\n',tostring(table.concat(data_rec, ", ")))
end

function segment.terminate()
    ion_count = ion_count+1
end 