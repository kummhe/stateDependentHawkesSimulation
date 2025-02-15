# Simulating market microstructure with state dependent hawkes process simulation

This is the code behind the article Market microsructure simulation with state-dependent Hawkes process.

Three codes are supplied with it:
- Client.py
- CTXPyClient.py
- MarketSimulator.py

In order to run the simulator, an instance of Ivan Jericevich's CoinTossX, that can be found in https://github.com/dharmeshsing/CoinTossX.
The repository has not been updated for a while, hence a few dependencies may be broken when building with Gradle. A few fixes that were necessary by the time I ran the simulations were:
1. Force the implementation of: 'com.google.guava:guava:20.0'. Or else you may get the "Could not resolve all files for configuration" error.
2. Use org.mapdb on the specific version '3.0.10'. Other versions have been compiled with an incompatible version of Java and will cause a conflict.

Next, you will need to install mpoints, the library that very efficiently implements State-Dependent Hawkes process and makes it substatially easier to use in python. The package is available at https://pypi.org/project/mpoints/.

Finally, make sure to update the variables jar_directory in CTXPyClient.py and ctxClient in Client.py to direct them to the location where CointossX was previously built.

When all is set, just run Client.py from a command promt using "python Client.py".
