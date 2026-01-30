================================================================================
TEST FORGE FRAMEWORK - COMPACT SUMMARY
================================================================================

QUICK OVERVIEW
================================================================================
Test Forge is a Python-based Active Directory testing framework with a GUI that
automates validation of AD infrastructure (Domain Controllers, Certificate 
Authorities, Member Servers).

================================================================================
ARCHITECTURE AT A GLANCE
================================================================================

GUI Layer (Tkinter)
  - Test selection & execution UI
  - Real-time log viewer
  - Status display
         |
         v
Test Execution Layer
  - Auto-discover test suites
  - Run test methods sequentially
  - Track PASS/FAIL/ERROR results
         |
         v
Server & Interface Layer
  - ServerManager (manages all servers)
  - DomainController, CA, MemberServer objects
  - Command interfaces (ADInterface, DCInterface)
         |
         v
PowerShell Execution Layer
  - Local execution (PowerShell class)
  - Remote execution (PowershellRemote class)
         |
         v
Windows PowerShell / AD Commands

================================================================================
CORE COMPONENTS
================================================================================

1. CONFIGURATION (config.py)
   - Global paths and constants
   - Project directory structure
   - Execution status definitions

2. SERVERS (library/setup/device/)
   - ADServer - Base server class
   - DomainController - DC-specific logic
   - CertificateAuthority - CA server
   - MemberServer - Regular member server
   - ServerManager - Orchestrates all servers

3. INTERFACES (library/setup/interface/)
   - ADInterface - Generic AD commands
   - DCInterface - Domain Controller commands
   - CAInterface - Certificate Authority commands
   - Maps PowerShell commands to Python methods

4. POWERSHELL EXECUTION (library/util/powershell.py)
   - PowerShell - Local command execution
   - PowershellRemote - Remote command execution via Invoke-Command
   - Parses output to Python dicts

5. TEST FRAMEWORK (library/test/)
   - BaseTest - Base class for all test suites
   - TestExecutor - Auto-discovers and executes tests
   - test_suite/ - Individual test suite files (auto-discovered)

6. UI (library/ui/main.py)
   - ADInstall - Main Tkinter application
   - File selection, test dropdown, start button
   - Real-time log display
   - Status bar with execution info

7. UTILITIES (library/util/)
   - parser.py - Parse XML/INI configuration files
   - powershell.py - PowerShell command execution
   - log.py - Logging system with file + GUI handlers
   - exception.py - Custom exception types

================================================================================
CONFIGURATION FILES
================================================================================

SERVER.INI - Infrastructure Setup
-------------------------------------
[Domain Controller 1]
    hostname = BDPK6DOMCTRL01
    ip = 192.168.1.1
    execution_host = true
    primary = true

[Domain Controller 2]
    hostname = BDPK6DOMCTRL02
    ip = 192.168.1.2
    execution_host = false
    primary = false

[Certificate Authority]
    hostname = BDPK6CERTAUTH01
    ip = 192.168.1.3

[Member Server]
    hostname = BDPK6WPMASM01
    ip = 192.168.1.4

Key Concepts:
- execution_host: The server where test commands execute locally
- primary: Primary domain controller designation


ACTIVEDIRECTORY_BDPK5.XML - AD Configuration
-------------------------------------
Defines:
- Domain name & NetBIOS
- User accounts with roles
- Organizational Units (OUs)
- Security groups
- Certificate Authority setup
- DNS and NTP configuration

================================================================================
EXECUTION FLOW
================================================================================

1. User runs: python start.py
   => ADInstall GUI launches

2. User selects XML config file
   => Parsed and validated

3. User selects test suite from dropdown
   => TestExecutor discovered available test suites

4. User clicks "Start"
   => Test runs in background thread:
      a) ServerManager loads servers from INI
      b) Test suite class instantiated with servers
      c) setup() method runs (parses XML)
      d) Each test_* method executes in order
      e) Results tracked (PASS/FAIL/ERROR)
      f) GUI updated with status & logs

5. Test completes
   => Status bar shows execution time
      Test results logged to file

================================================================================
TEST SUITE STRUCTURE
================================================================================

CREATING A TEST SUITE
File: library/test/test_suite/test_custom.py

from library.test.test_suite.base_test import BaseTest

class TestCustom(BaseTest):
    def setup(self):
        super().setup()
        # Optional setup
        
    def test_verify_domain_name(self):
        """Test method (auto-discovered)"""
        domain = self.primary_dc.ad_interface.get_ad_root_domain_name()
        expected = self.adinstall_dict['Config']['Park']['ActiveDirectory']['DomainName']
        assert domain == expected, f"Domain mismatch"
        
    def test_verify_dc_count(self):
        """Another test method"""
        # Access servers via self.primary_dc, self.secondary_dc, self.ca, self.ms
        pass


AUTO-DISCOVERY RULES
- File must start with 'test_'
- Class must start with 'Test'
- Class must inherit from 'BaseTest'
- Test methods must start with 'test_'

================================================================================
KEY DESIGN PATTERNS
================================================================================

PATTERN              USAGE
------               -----
Strategy             Choose PowerShell vs PowershellRemote execution
Factory              Auto-discover and instantiate test suites
Template Method      BaseTest defines test skeleton
Dependency Injection Pass server instances to test classes
Observer             GUI callbacks for test status updates
Singleton            Single Log instance for whole app

================================================================================
SERVER ACCESS IN TESTS
================================================================================

Access server instances:
  self.primary_dc              # Primary Domain Controller
  self.secondary_dc            # Secondary Domain Controller
  self.ca                      # Certificate Authority
  self.ms                      # Member Server

Execute commands:
  result = self.primary_dc.powershell.run_command("Get-ADUser -Filter *")

Use interfaces:
  domain = self.primary_dc.ad_interface.get_ad_root_domain_name()
  forest = self.primary_dc.ad_interface.get_adforest()

Access configuration:
  self.adinstall_dict          # Parsed ActiveDirectory_BDPK5.xml

================================================================================
EXECUTION STRATEGIES
================================================================================

LOCAL EXECUTION (Execution Host)
  PowerShell() => Subprocess execution on local machine

REMOTE EXECUTION
  PowershellRemote("hostname") => Invoke-Command to remote PowerShell

Selection: Automatic based on 'execution_host' flag in server.ini

================================================================================
TEST RESULT TYPES
================================================================================

STATUS    MEANING
------    -------
PASS      Test completed, all assertions passed
FAIL      AssertionError raised (expected failure)
ERROR     Unexpected exception raised

================================================================================
FILE ORGANIZATION
================================================================================

test_forge/
  ├── start.py                          # Entry point
  ├── config.py                         # Global configuration
  ├── server.ini                        # Server definitions
  ├── library/
  │   ├── setup/
  │   │   ├── device/                   # Server classes
  │   │   ├── interface/                # Command interfaces
  │   │   └── server_manager.py
  │   ├── test/
  │   │   ├── test_executor.py          # Orchestrator
  │   │   └── test_suite/               # Test files (auto-discovered)
  │   ├── ui/
  │   │   └── main.py                   # Tkinter GUI
  │   └── util/
  │       ├── parser.py, powershell.py, log.py, exception.py
  ├── resource/
  │   └── ActiveDirectory_BDPK5.xml     # AD config
  ├── log/                              # Execution logs
  └── UNIT_TEST.py                      # Testing utilities

================================================================================
COMMON OPERATIONS
================================================================================

ADD NEW TEST SUITE
1. Create library/test/test_suite/test_feature.py
2. Define class TestFeature(BaseTest)
3. Add def test_*(self) methods
4. Auto-discovered on next run

ADD NEW POWERSHELL COMMAND
1. Add method to appropriate Interface class
2. Use self.powershell_obj.run_command("PowerShell command")
3. Parse and return result
4. Call from test via server interface

ADD NEW SERVER TYPE
1. Create class extending ADServer
2. Add section to server.ini
3. Register in ServerManager._initialize_servers()
4. Create interface if needed

================================================================================
EXTENSION OPPORTUNITIES
================================================================================

- Multi-format configs: JSON, YAML, TOML support
- Plugin system: Load test suites dynamically
- Advanced logging: Structured logs, remote logging
- Parallel execution: Run tests concurrently
- Reports: HTML, JUnit XML output
- Monitoring: Performance metrics, health checks
- Database: Persist test results
- Retry logic: Handle transient failures
- Test parameterization: Run same test with different inputs

================================================================================
TROUBLESHOOTING
================================================================================

ISSUE                    FIX
-----                    ---
Test not discovered      Check class name starts with 'Test', 
                         inherits 'BaseTest'
PowerShell fails         Test command directly in PowerShell
GUI freezes              Tests should run in separate thread
Config not found         Verify file path in config.py
Permission denied        Check write access to log/ directory

================================================================================
QUICK START
================================================================================

1. Ensure server.ini and ActiveDirectory_BDPK5.xml exist

2. Run application
   python start.py

3. In GUI:
   - Click "Select ADInstall xml" => choose config file
   - Select test suite from dropdown
   - Click "Start" => watch logs for results

================================================================================
KEY ENTRY POINT
================================================================================

start.py
---------
from library.ui.main import ADInstall

if __name__ == "__main__":
    ad_install = ADInstall()
    ad_install.mainloop()

This simple entry point initializes the ADInstall GUI and starts the 
event loop. All initialization happens in ADInstall.__init__():
  - Log system setup
  - ServerManager initialization (loads servers from INI)
  - TestExecutor initialization (auto-discovers test suites)
  - UI widget creation

================================================================================
BUILT FOR AD INFRASTRUCTURE VALIDATION WITH EXTENSIBILITY FOR CUSTOM 
TESTING NEEDS
================================================================================