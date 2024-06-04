import winreg
import os

def query_winreg(winreg_key, values_to_replace : list, replace_with : str, subkey : str ="") -> None:
  """Search words in the Windows Registry and replace it with a specific replacement word.
  
  Parameters:
  winreg_key : root registry key to fully traverse
  values_to_replace (list): array of strings to search for in the registry
  replace_with (str): value to replace the search_terms with in the registry
  subkey (str): used to start from specific path, if not specified, it will start from root 

  Returns:
  None
  """
  root = None
  try:
    root = winreg.OpenKey(winreg_key, subkey)
    subkeys = []
    # retrieve all the subdirectories
    for folder in range(winreg.QueryInfoKey(root)[0]):
            subkeys.append(winreg.EnumKey(root, folder))
    
    if len(subkeys) > 0:
        for entry in subkeys:
          # search recursively
          new_subkey = os.path.join(subkey, entry)
          query_winreg(winreg_key, values_to_replace, replace_with, new_subkey)

    # replace value
    # get amount of values
    (_, amount_of_values, _) = winreg.QueryInfoKey(root)
    # iterate over values
    for index_of_value in range(amount_of_values):
      # get value information
      name, _, type = winreg.EnumValue(root, index_of_value)
      # retrieve the value
      value, value_type = winreg.QueryValueEx(root, name)
      # check only the string types
      if value_type == winreg.REG_SZ:
        # check if any string needs replacing
        for term in values_to_replace:
          if term in value:
            # replace the value
            new_val = value.replace(term, replace_with)
            print(f"{value} -> {new_val}")
            winreg.SetValue(root, index_of_value, winreg.REG_SZ, new_val)
  except Exception as e:
     pass # print(f"error occurred while opening key: {e}")
  finally:
    if root is not None:
      winreg.CloseKey(root)

if __name__ == "__main__":
  print("""WARNING: You are about to change a possibly system-breaking part of Windows
        Please make sure to have a backup of Windows Registry before running this script.""")
  answer = input("Are you sure you want to continue? (y/n)?")
  answer = answer.strip().lower()
  if answer == "y":
    to_replace = ["VirtualBox", "VMWare", "VBox", "QEMU"]
    replacer = "Lenovo"
    print("### Started cleaning HKEY_LOCAL_MACHINE")
    query_winreg(winreg.HKEY_LOCAL_MACHINE, to_replace, replacer)
    print("### Started cleaning HKEY_CURRENT_USER")
    query_winreg(winreg.HKEY_CURRENT_USER, to_replace, replacer)
    print("### Done")
  else:
    print("Aborted, nothing changed to Windows Registry")
