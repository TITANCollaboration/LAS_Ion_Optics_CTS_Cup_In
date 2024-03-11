simion.workbench_program()

adjustable ext_steery = 0
adjustable ext_steerz = 0
adjustable bender = 900
adjustable sel_focus = -2300
adjustable sel_x = 0
adjustable sel_z = 0
adjustable capture_focus = -900
adjustable capture_x = 0
adjustable capture_z = 0
adjustable capture_dec = 700
adjustable iRFQ = 1300

function segment.fast_adjust()
  -- set the extraction steerers
  adj_elect6 = -ext_steerz
  adj_elect7 = -ext_steery
  adj_elect8 = ext_steerz
  adj_elect9 = ext_steery
  -- set bender with only a few buttons
  adj_elect10 = bender
  adj_elect20 = -bender
  adj_elect30 = -bender
  adj_elect40 = bender
  -- set SEL steering
  adj_elect101 = sel_focus + sel_z
  adj_elect102 = sel_focus - sel_x
  adj_elect103 = sel_focus - sel_z
  adj_elect104 = sel_focus + sel_x
  -- set capture electrode focus
  adj_elect203 = capture_focus
  -- set steering in capure optics to be symmetric
  adj_elect221 = -capture_x
  adj_elect222 = capture_x
  adj_elect223 = -capture_z
  adj_elect224 = capture_z
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

function segment.other_actions()
end
