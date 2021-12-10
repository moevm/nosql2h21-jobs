#%%
import app
import pathlib
#%%
root = pathlib.Path("")
config_path = (root/"configs"/"config.json").resolve()
#%%
this_tbh = app.create_app(config_path.resolve().as_posix())
this_tbh
#%%
this_tbh.run(host = "0.0.0.0", port=5000)

#%%
print("done")

if __name__ == "__main__":
    pass
#%%