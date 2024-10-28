import DaVinciResolveScript as dvr_script

def test_resolve():
    try:
        resolve = dvr_script.scriptapp("Resolve")
        if resolve is None:
            print("Error: Could not get resolve instance.")
        else:
            print("Successfully got Resolve instance.")
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    test_resolve()
