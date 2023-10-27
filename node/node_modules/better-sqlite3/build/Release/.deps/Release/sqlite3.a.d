cmd_Release/sqlite3.a := ln -f "Release/obj.target/deps/sqlite3.a" "Release/sqlite3.a" 2>/dev/null || (rm -rf "Release/sqlite3.a" && cp -af "Release/obj.target/deps/sqlite3.a" "Release/sqlite3.a")
