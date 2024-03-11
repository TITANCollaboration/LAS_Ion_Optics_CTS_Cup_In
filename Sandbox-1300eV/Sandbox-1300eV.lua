simion.workbench_program()

adjustable ext_steery = 0
adjustable ext_steerz = 0
adjustable bender = 900
adjustable sel_focus = -2300
adjustable sel_x = 0
adjustable sel_z = 0

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
end

function segment.other_actions()
end
