-- our fake protocol
local wpanlookup = Proto("wpanlookup", "WPAN Lookup")

-- register fields to the protocol
-- wpanlookup.fields = {
--     f_dstname,
--     f_dst,
--     f_srcname,
--     f_src,
--     f_test
-- }

function split(s, delimiter)
    result = {};
    for match in (s..delimiter):gmatch("(.-)"..delimiter) do
        table.insert(result, match);
    end
    return result;
end

function GetKeyFileName()
   local str = debug.getinfo(2, "S").source:sub(2)
   return tostring( str:match("(.*)(lua)").."key.csv" )
end
 
function ReadKey()  
    lookup_table = {}
    for line in io.lines( GetKeyFileName() ) do 
       lookup_table[#lookup_table + 1] = line
    end
    return table.concat(lookup_table, "")
end

local function hexdecode(hex)
    hex = hex:gsub( "%W", "" )
    return (hex:gsub("%x%x", function(digits) return string.char(tonumber(digits, 16)) end))
end

function xorf(data)
  local d = {}
  local dt = {}
  local on = false
  for i = 1, data:len() do
      local x = bit32.bxor(data:byte(i), data:byte(data:len() - 3))
      local c = hexdecode(string.format("%02x", x))
      table.insert(dt, c)
  end
  
  
  return table.concat(dt, "")
end

function wpanlookup.dissector(tvb, pinfo, tree)
      
    -- Add a new protocol tree for out fields
    local subtree = tree:add(wpanlookup)
    subtree:add("data", xorf(tvb(0, tvb:len()):string()) )
end

function file_exists(name)
   local f=io.open(name,"r")
   if f~=nil then io.close(f) return true else return false end
end

-- Ensure that our dissector is invoked after dissection of a packet.
register_postdissector(wpanlookup)