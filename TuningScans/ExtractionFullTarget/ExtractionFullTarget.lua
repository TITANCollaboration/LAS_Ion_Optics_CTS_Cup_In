--[[
    ExtractionSteering2DScan.lua - scan the intitial ion start position and the extraction steering and record the ion's displacement from the ion axis in the SEL
]]

simion.workbench_program()

local extlens1_center = -2500       -- voltage for extraction y,z steering at center of target
local extlens1_range = 100     -- Range of focus voltages

local extlens2_center = 1500       -- voltage for extraction y,z steering at center of target
local extlens2_range = 100     -- Range of focus voltages

local nvolts = 25         -- number of voltages in focus scan range (increment = (2*range)/(n-1)) 26

local data_rec       -- tracks the data to be written to file    

-- ion optics tuning
local ext_energy = 1300     -- voltage on ion target (defines beam energy)
local ext_lens1 = 0      -- voltage on 3rd extraction electrode (first einzel lens)
local ext_lens2 = 0         -- voltage on 5th extraction electrode (second einzel lens)
local ext_y = 0             -- voltage on y axis steering of 6th extraction electrode quad (symmetric steering)
local ext_z = 0             -- voltage on z axis steering of 6th extraction electrode quad (symmetric steering)
local bender = 0            -- Bender Voltage
local sel_focus = 0      -- common voltage on sel for focus

-- figure out spacing of spots
extlens1_inc = (2*extlens1_range)/(nvolts-1)
extlens2_inc = (2*extlens2_range)/(nvolts-1)

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

    file = io.open("data\\ke_20\\2DIonExtractionLens_ke_20_V12_"..extlens1_center.."_"..extlens2_center.."_nvolts_"..nvolts..".csv", "w")
    file:write("Generated from ExtractionFullTarget.iob\n Extraction Lens1, Extraction Lens2,Efficiency, mean dist, median dist, max dist, min dist")
            
    for ex1 = 1,nvolts do
        ext_lens1 = extlens1_center - extlens1_range + (ex1-1)*extlens1_inc
        for ex2 = 1, nvolts do 
          ext_lens2 = extlens2_center - extlens2_range + (ex2-1)*extlens2_inc
          data_rec = {ext_lens1,ext_lens2,nil,nil,nil, nil,nil}
          print("lens1: " ..ext_lens1.. "\nlens2: "..ext_lens2)
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

  if (ion_px_mm >= 101.625 and rec_pos ~= ion_number)
  then
    dist[#dist+1] = (abs(ion_py_mm - 35)^2 + abs(ion_pz_mm - 35)^2)^0.5
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